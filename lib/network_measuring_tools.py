import networkx as nx

def calc_global_clustering_coefficient(G: nx.Graph) -> float:
    return nx.average_clustering(G)

def calc_average_path_length(G: nx.Graph) -> float:
    return nx.average_shortest_path_length(G)

def calc_average_degree(G: nx.Graph) -> float:
    return sum(dict(G.degree()).values()) / len(G) 

def calc_network_diameter(G: nx.Graph) -> float:
    return nx.diameter(G)

def calc_average_degree_connectivity(G: nx.Graph) -> float:
    return nx.average_degree_connectivity(G)

def calc_average_neighbor_degree(G: nx.Graph) -> float:
    return nx.average_neighbor_degree(G)

def calc_local_efficiency(G: nx.Graph) -> float:
    return nx.local_efficiency(G)

def calc_global_efficiency(G: nx.Graph) -> float:
    return nx.global_efficiency(G)
