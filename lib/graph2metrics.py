from dataclasses import dataclass
from typing import Any, List, NamedTuple, Tuple
import networkx as nx
from lib.network_measuring_tools import *

@dataclass
class Params:
    rho: float
    nu: float
    recentness: float
    frequency: float
    steps: int

class Metrics(NamedTuple):
    global_cluster_coefficient: float
    average_path_length: float
    average_degree: float
    network_diameter: float
    average_degree_connectivity: float
    average_neighbor_degree: float
    local_efficiency: float
    global_efficiency: float

class Graph2Metrics:
    def graph2metrics(self, graph: nx.Graph) -> Metrics:
        
        return Metrics(global_cluster_coefficient=calc_global_clustering_coefficient(graph),
                       average_path_length=calc_average_path_length(graph),
                       average_degree=calc_average_degree(graph),
                       network_diameter=calc_network_diameter(graph),
                       average_degree_connectivity=calc_average_degree_connectivity(graph),
                       average_neighbor_degree=calc_average_neighbor_degree(graph),
                       local_efficiency=calc_local_efficiency(graph),
                       global_efficiency=calc_global_efficiency(graph))