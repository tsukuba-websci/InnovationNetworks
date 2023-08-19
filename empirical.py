import pandas as pd
import networkx as nx
from collections import Counter
from typing import Any, NamedTuple
import os
from dataclasses import dataclass
from collections import defaultdict
from lib.utils import *

@dataclass
class Params:
    rho: float
    nu: float
    recentness: float
    friendship: float
    symmetry: float
    steps: int

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

def separate_graphs(G):
    # Create empty directed subgraphs
    G_no_good_idea = nx.DiGraph()
    G_has_good_idea = nx.DiGraph()

    # Populate subgraphs
    for node, attrs in G.nodes(data=True):
        if attrs['GoodIdea'] == 0:
            G_no_good_idea.add_node(node, **attrs)
        elif attrs['GoodIdea'] > 0:
            G_has_good_idea.add_node(node, **attrs)

    # Add edges relevant to the nodes present in each subgraph
    for u, v, edge_attrs in G.edges(data=True):
        if u in G_no_good_idea and v in G_no_good_idea:
            G_no_good_idea.add_edge(u, v, **edge_attrs)
        if u in G_has_good_idea and v in G_has_good_idea:
            G_has_good_idea.add_edge(u, v, **edge_attrs)

    return G_no_good_idea, G_has_good_idea

def df_to_metrics(df, metrics_location, interval_num):
    user_mapping = defaultdict(lambda: len(user_mapping))
    history = [(user_mapping[caller], user_mapping[callee]) for caller, callee in df[['caller', 'callee']].values]

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

    results = pd.DataFrame([result._asdict()])
    results.to_csv(metrics_location, index=False)
    
def df_to_metrics_incremental(df, metrics_location, interval_num):
    user_mapping = defaultdict(lambda: len(user_mapping))
    results = []

    for i in range(100, len(df) + 1):
        subset_df = df.head(i)
        history = [(user_mapping[caller], user_mapping[callee]) for caller, callee in subset_df[['caller', 'callee']].values]

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

        results.append(result)

    result_dicts = [result._asdict() for result in results]
    results_df = pd.DataFrame(result_dicts)
    results_df.to_csv(metrics_location, index=False)

def setup():
    # Load data
    user_network_data = pd.read_csv('data/input/UserNetworkData.csv', parse_dates=['Date'])[['F','T','Date']].head(20000)
    user_network_data = user_network_data.rename(columns={
    'F': 'caller',
    'T': 'callee'
    })

    idea_submission_data = pd.read_csv('data/input/IdeaSubmissionData.csv')

    # Get all unique statuses
    all_statuses = idea_submission_data['Status'].unique()

    # Create directed graph
    G = nx.from_pandas_edgelist(user_network_data, 'caller', 'callee')

    # Prepare dictionary to store status counts for each user
    user_status_counts = {}
    good_idea_counts = {}

    # Iterate through idea submissions and count unique statuses and good ideas for each user
    for index, row in idea_submission_data.iterrows():
        user = row['User']
        status = row['Status']
        good_idea = row['GoodIdea']
        
        if user not in user_status_counts:
            user_status_counts[user] = Counter({s: 0 for s in all_statuses})
        
        user_status_counts[user][status] += 1
        good_idea_counts[user] = good_idea_counts.get(user, 0) + good_idea

    # Assign count of unique status and good ideas to each node in the network
    for node in G.nodes():
        status_counts = user_status_counts.get(node, Counter({s: 0 for s in all_statuses}))
        for status, count in status_counts.items():
            G.nodes[node][status] = count
        G.nodes[node]['GoodIdea'] = good_idea_counts.get(node, 0)

    return user_network_data, idea_submission_data, G

def most_connected_subgraph(G) -> Any:
    connected_components = nx.connected_components(G)
    largest_connected_component = max(connected_components, key=len)
    largest_connected_subgraph = G.subgraph(largest_connected_component)
    return largest_connected_subgraph

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

def connected_users(user_network_data, G):
    node_ids = list(G.nodes)
    filtered_data = user_network_data[(user_network_data['caller'].isin(node_ids)) | (user_network_data['callee'].isin(node_ids))]
    return filtered_data

def csv_to_metrics(csv_location, metrics_location, interval_num: int) -> None:

    df = pd.read_csv(csv_location)
    user_mapping = defaultdict(lambda: len(user_mapping))
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

    df = pd.DataFrame([result._asdict()])
    df.to_csv(metrics_location, index=False)
    pass

if __name__ == '__main__':

    global thread_num
    setup_threads()
    Main = setup_julia()

    user_network_data, idea_submission_data, graph = setup()
    
    graph_to_json(graph, "data/output/graph/graph_empirical_full.json")
    df_to_csv(user_network_data, "data/output/history/history_empirical_full.csv")

    plot_degree_distributions(graph, "plot/degre_distribution_empirical.png")
    plot_clustering_coefficients(graph, "plot/clustering_coefficient_distribution_empirical.png")

    plot_degree_distributions_with_innovators(graph, "plot/degre_distribution_with_innovators_empirical.png")
    plot_clustering_coefficients_with_innovators(graph, "plot/clustering_coefficient_distribution_with_innovators_empirical.png")

    largest_subgraph = most_connected_subgraph(graph)
    largest_subgraph_users = connected_users(user_network_data, graph)

    graph_to_json(largest_subgraph, "data/output/graph/graph_empirical.json")
    df_to_csv(largest_subgraph_users, "data/output/history/history_empirical.csv")

    csv_to_metrics("data/output/history/history_empirical.csv",'data/output/metrics/ideastorm.csv', 1000)

    innovation_graph, no_innovation_graph = separate_graphs(graph)
    graph_to_json(innovation_graph, "data/output/graph/innovation_graph.json")
    graph_to_json(no_innovation_graph, "data/output/graph/no_innovation_graph.json")

    plot_degree_distributions(innovation_graph, "plot/innovation_graph.png")
    plot_degree_distributions(no_innovation_graph, "plot/no_innovation_graph.png")

    df_to_metrics_incremental(user_network_data[['caller', 'callee']], 'data/output/metrics/test.csv',50)