using PolyaUrnSimulator
using DataFrames, CSV
using Graphs
using StatsBase
using Base.Threads
using PyCall

struct LabelHistoryRecord
    birthstep::Int
    src::Int
    dst::Int
end

function initialize_env_and_agents(rho::Int, nu::Int, s::String, get_caller::Function)::Tuple{Environment, Vector{Agent}}

    if s == "asw"
        env = Environment(; get_caller, who_update_buffer=:caller)
        init_agents = [
            Agent(rho, nu, ssw_strategy!)
            Agent(rho, nu, ssw_strategy!)
        ]
    elseif s == "wsw"
        env = Environment(; get_caller)
        init_agents = [
            Agent(rho, nu, wsw_strategy!)
            Agent(rho, nu, wsw_strategy!)
        ]
    else
        throw(error("strategy must be asw or wsw"))
    end

    env.history = [(1,2)]
    return env, init_agents
end

"""
waves of novelties モデル(proposed)
"""
function run_waves_model(
    rho::Int,
    nu::Int,
    s::String,
    zeta::Float64,
    eta::Float64;
    steps=10,
    nodes=100,
    on_classify::Union{Function,Nothing}=nothing,
    on_weight::Union{Function,Nothing}=nothing,
)::Tuple{Environment,Vector{Int},Vector{LabelHistoryRecord}}
    function f(N_k::Int, N_not_k::Int, zeta::Real)
        return N_k / (N_k + zeta * N_not_k)
    end

    function g(N_k::Int, N_not_k::Int, zeta::Real)
        return (N_k + zeta * f(N_k, N_not_k, zeta) * N_not_k) / (N_k + zeta * N_not_k)
    end

    last_label = 3
    labels = Int[[1, 1]; ones(Int, nu + 1) .* 2; ones(Int, nu + 1) .* 3]
    label_tree = LabelHistoryRecord[]

    unique_history = Vector{Int}()

    """callerエージェントになったか否かのビット列"""
    became_caller = BitVector()

    function get_caller(env::Environment)::Int
        append!(became_caller, zeros(length(env.rhos) - length(became_caller)))

        # 最初は履歴が無いのでデフォルトのget_callerを使う
        if length(env.history) == 0
            next_caller = PolyaUrnSimulator.get_caller(env)
            became_caller[next_caller] |= 1
            return next_caller
        end

        caller, _ = env.history[end]

        # 壺のサイズが0より大きいエージェントを抽出
        all_agents = collect(1:length(env.buffers))[.!isempty.(env.buffers)]
        all_agents_labels = labels[all_agents]
        all_agents_became_caller = became_caller[all_agents]

        # 1ステップ前のcallerエージェントと同じラベルを持つエージェントを抽出
        k_indices = all_agents_labels .== labels[caller]

        # 今まで一度以上callerになったことのあるエージェントを抽出
        novelty_indices = .!all_agents_became_caller

        C1 = collect(1:length(env.buffers))[isempty.(env.buffers)]
        C2 = all_agents[.!novelty_indices .* k_indices]
        C3 = all_agents[.!novelty_indices .* .!k_indices]
        C4 = all_agents[novelty_indices .* k_indices]
        C5 = all_agents[novelty_indices .* .!k_indices]

        if on_classify !== nothing
            on_classify(C1, C2, C3, C4, C5)
        end

        N_k = sum(k_indices)
        N_not_k = sum(.!k_indices)

        wv = Weights(zeros(length(env.buffers)))

        wc2 = 1
        wc3 = zeta * f(N_k, N_not_k, zeta)
        wc4 = g(N_k, N_not_k, zeta)
        wc5 = eta * g(N_k, N_not_k, zeta)

        if on_weight !== nothing
            on_weight(wc2, wc3, wc4, wc5)
        end

        wv[C2] .= wc2
        wv[C3] .= wc3
        wv[C4] .= wc4
        wv[C5] .= wc5

        next_caller = sample(1:length(env.buffers), wv)
        became_caller[next_caller] |= 1
        return next_caller
    end

    env, init_agents = initialize_env_and_agents(rho, nu, s, get_caller)
    init!(env, init_agents)

    for step in 1:steps
        step!(env)
    
        caller, callee = env.history[end]
        if !(callee in unique_history)
            append!(labels, ones(nu + 1) * (last_label + 1))
            push!(label_tree, LabelHistoryRecord(step, labels[callee], last_label + 1))
            
            last_label = last_label + 1
        end
        push!(unique_history, caller, callee)
        
        num_nodes = length(Set([item for sublist in env.history for item in sublist]))
        if num_nodes == nodes
            break
        end
    end
    
    return env, labels, label_tree
end

mutable struct Params
    rho::Int
    nu::Int
    s::String
    zeta::Float64
    eta::Float64
    steps::Int
    nodes::Int
    thread_num::Int
end

function convert_to_params(py_params::Vector{PyObject})
    return [begin
        rho = py_p["rho"]
        nu = py_p["nu"]
        s = py_p["s"]
        zeta = py_p["zeta"]
        eta = py_p["eta"]
        steps = py_p["steps"]
        nodes = py_p["nodes"]
        thread_num = py_p["thread_num"]
        Params(rho, nu, s, zeta, eta, steps, nodes, thread_num)
    end for py_p in py_params]
end

function parallel_run_waves_model(py_params_list::Vector{PyObject})
    params_list = convert_to_params(py_params_list)
    num_params = length(params_list)
    ret = Vector{Any}(undef, num_params)
    lk = ReentrantLock()
    Threads.@threads for id in 1:num_params
        p = params_list[id]
        
        try
            a, b, c = run_waves_model(p.rho, p.nu, p.s, p.zeta, p.eta, steps=p.steps, nodes=p.nodes)
            local_history = copy(a.history)
            lock(lk) do
                ret[id] = local_history
            end
        catch error
            lock(lk) do
                ret[id] = []  # Assign an empty array as a fallback
            end
        end
    end

    # Check for any uninitialized values in ret
    for (idx, value) in enumerate(ret)
        if !isassigned(ret, idx)
            ret[idx] = []  # Assign an empty array for any uninitialized values
        end
    end

    return ret
end