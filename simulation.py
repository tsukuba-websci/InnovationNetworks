from typing import Any, List, NamedTuple, Tuple
from rsurn import Environment, EnvironmentGene
import random
from dataclasses import dataclass
from utils.utils import *

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
    return env.history

def run_and_save_model(params, runs=8):
    for i in range(1, runs + 1):
        history = run_model(params)
        history_csv_path = f"data/output/history/history_simulation_{i}.csv"
        history_to_csv(history, history_csv_path)

        graph = history_to_graph(history_csv_path)
        graph_json_path = f"data/output/graph/graph_simulation_{i}.json"
        graph_to_json(graph, graph_json_path)

if __name__ == '__main__':
    # steps = 20000
    # params = Params(1,3, 0, 0, 0, steps)
    # history = run_model(params)
    # history_to_csv(history, "data/output/history/history_simulation.csv")
    # graph = history_to_graph("data/output/history/history_simulation.csv")
    # graph_to_json(graph, "data/output/graph/graph_simulation.json")
    # plot_degree_distributions(graph, "plot/degre_distribution_simulation.png")
    # plot_clustering_coefficients(graph, "plot/clustering_coefficient_distribution_simulation.png")

    steps = 10000
    params = Params(10,6, 0, 0, 0, steps)
    run_and_save_model(params, 8)