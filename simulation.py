from typing import Any, List, NamedTuple, Tuple
from rsurn import Environment, EnvironmentGene
import random
from dataclasses import dataclass
from lib.utils import *
from collections import defaultdict
import os

@dataclass
class Params:
    rho: float
    nu: float
    recentness: float
    friendship: float
    symmetry: float
    steps: int

class History2VecResult(NamedTuple):
    gamma: float
    no: float
    nc: float
    oo: float
    oc: float
    c: float
    y: float
    g: float
    r: float
    h: float

def run_model(params: Params) -> Tuple[List[Tuple[int, int]], float]:
    rho = int(params.rho)
    nu = int(params.nu)
    gene = EnvironmentGene(rho, nu, params.recentness, params.friendship, params.symmetry)
    env = Environment(gene)
    caller = random.choice([0, 1])  
    for _ in range(params.steps):
        callee = env.get_callee(caller)
        env.interact(caller, callee)
        caller = callee
        num_nodes = len(set([item for tup in env.history for item in tup]))
        if num_nodes == 10:
            break
    return convert_tuples(env.history)

def run_and_save_model(params, runs=8):
    for i in range(1, runs + 1):
        history = run_model(params)
        history_csv_path = f"data/output/history/history_simulation_{i}.csv"
        history_to_csv(history, history_csv_path)

        graph = history_to_graph(history_csv_path)
        graph_json_path = f"data/output/graph/graph_simulation_{i}.json"
        graph_to_json(graph, graph_json_path)

def csv_to_metrics(csv_location, metrics_location, interval_num: int) -> None:

    # Read CSV file
    df = pd.read_csv(csv_location)

    # Create a mapping of unique users to unique integers
    user_mapping = defaultdict(lambda: len(user_mapping))

    # Convert DataFrame to list of tuples
    history = [(user_mapping[caller], user_mapping[callee]) for caller, callee in df.values]

    if any(map(lambda row: row[0] == 0 or row[1] == 0, history)):
        history = list(map(lambda row: (row[0] + 1, row[1] + 1), history))

    nt = Main.history2vec(history, interval_num)

    result = History2VecResult(
        c=nt.c,
        g=nt.g,
        gamma=nt.gamma,
        h=nt.h,
        nc=nt.nc,
        no=nt.no,
        oc=nt.oc,
        oo=nt.oo,
        r=nt.r,
        y=nt.y,
    )

    # Convert the result to a DataFrame
    df = pd.DataFrame([result._asdict()])

    # Save the DataFrame to a csv
    df.to_csv(metrics_location, index=False)
    pass

def setup_threads():
    global thread_num
    JULIA_NUM_THREADS = "JULIA_NUM_THREADS"
    if JULIA_NUM_THREADS not in os.environ:
        cpu_count = os.cpu_count()
        if cpu_count is not None:
            thread_num = cpu_count
        else:
            thread_num = 4  # default thread number
        os.environ[JULIA_NUM_THREADS] = str(thread_num)
    else:
        thread_num = int(os.environ[JULIA_NUM_THREADS])

    print(f"run with {thread_num} thread(s)")

def setup_julia():
    from julia.api import Julia

    Julia(compiled_modules=False)

    from julia import Pkg  # type: ignore

    Pkg.activate(".")  # use ./Project.toml
    Pkg.add("StatsBase")
    Pkg.add(url="/Users/ciaran/dev/DynamicNetworkMeasuringTools/", rev="add-higher-order-heaps")
    Pkg.update()
    Pkg.instantiate()  # install dependencies

    from julia import Main

    Main.include("Main.jl")
    print("Finish setup Julia.")
    return Main

if __name__ == '__main__':

    global thread_num
    setup_threads()
    Main = setup_julia()

    # steps = 20000
    # params = Params(18,5, 0, 0, 0, steps)
    # history = run_model(params)
    # history_to_csv(history, "data/output/history/history_simulation.csv")
    # graph = history_to_graph("data/output/history/history_simulation.csv")
    # graph_to_json(graph, "data/output/graph/graph_simulation.json")

    # csv_to_metrics("data/output/history/history_simulation.csv",'data/output/metrics/simulation.csv', 1000)


    # plot_degree_distributions(graph, "plot/degre_distribution_simulation.png")
    # plot_clustering_coefficients(graph, "plot/clustering_coefficient_distribution_simulation.png")

    # Run the model multiple times for a given param

    steps = 50000
    params = Params(18,5, 0, 0, 0, steps)
    run_and_save_model(params, 8)