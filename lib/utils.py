import pandas as pd
from typing import Any
import matplotlib.pyplot as plt
import csv
import json
import pandas as pd
import networkx as nx
from typing import Any, NamedTuple
import csv
import os
from lib.graph2metrics import Metrics

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

def plot_degree_distributions(G: Any, location) -> None:
    all_degrees = [deg for node, deg in G.degree()]

    fig, axs = plt.subplots(figsize=(10, 10))

    axs.hist(all_degrees, bins=500, alpha=0.5, color='blue')
    axs.set_title('Degree Distribution of All Nodes')
    axs.set_xlabel('Degree')
    axs.set_ylabel('Number of Nodes')

    plt.tight_layout()
    plt.savefig(location)

def plot_degree_distributions_with_innovators(G: Any, location) -> None:
    all_degrees = [deg for node, deg in G.degree()]
    good_idea_degrees = [deg for node, deg in G.degree() if G.nodes[node]['GoodIdea'] > 0]

    fig, axs = plt.subplots(2, figsize=(10, 10))

    axs[0].hist(all_degrees, bins=500, alpha=0.5, color='blue')
    axs[0].set_title('Degree Distribution of All Nodes')
    axs[0].set_xlabel('Degree')
    axs[0].set_ylabel('Number of Nodes')

    axs[1].hist(good_idea_degrees, bins=500, alpha=0.5, color='green')
    axs[1].set_title('Degree Distribution of Innovators')
    axs[1].set_xlabel('Degree')
    axs[1].set_ylabel('Number of Nodes')

    plt.tight_layout()
    plt.savefig(location)

def plot_clustering_coefficients(G: Any, location) -> None:
    clustering_coeffs_all = nx.clustering(G)
    coeff_values_all = list(clustering_coeffs_all.values())

    fig, axs = plt.subplots(figsize=(10, 10))

    axs.hist(coeff_values_all, bins=20, edgecolor='black', color='blue', alpha=0.5)
    axs.set_title('Clustering Coefficient Distribution of All Nodes')
    axs.set_xlabel('Clustering Coefficient')
    axs.set_ylabel('Number of Nodes')

    plt.tight_layout()
    plt.savefig(location)

def plot_clustering_coefficients_with_innovators(G: Any, location) -> None:
    clustering_coeffs_all = nx.clustering(G)
    coeff_values_all = list(clustering_coeffs_all.values())

    clustering_coeffs_good_idea = {node: coeff for node, coeff in clustering_coeffs_all.items() if G.nodes[node]['GoodIdea'] > 0}
    coeff_values_good_idea = list(clustering_coeffs_good_idea.values())

    fig, axs = plt.subplots(2, figsize=(10, 10))

    min_val = min(min(coeff_values_all), min(coeff_values_good_idea))
    max_val = max(max(coeff_values_all), max(coeff_values_good_idea))

    axs[0].hist(coeff_values_all, bins=20, range=(min_val, max_val), edgecolor='black', color='blue', alpha=0.5)
    axs[0].set_title('Clustering Coefficient Distribution of All Nodes')
    axs[0].set_xlabel('Clustering Coefficient')
    axs[0].set_ylabel('Number of Nodes')
    axs[0].set_xlim([min_val, max_val])

    axs[1].hist(coeff_values_good_idea, bins=20, range=(min_val, max_val), edgecolor='black', color='green', alpha=0.5)
    axs[1].set_title('Clustering Coefficient Distribution of Nodes with Good Ideas')
    axs[1].set_xlabel('Clustering Coefficient')
    axs[1].set_ylabel('Number of Nodes')
    axs[1].set_xlim([min_val, max_val])

    plt.tight_layout()
    plt.savefig(location)

def history_to_graph(csv_location) -> Any:
    df = pd.read_csv(csv_location)
    G = nx.from_pandas_edgelist(df, 'caller', 'callee')
    return G

def history_object_to_graph(history) -> Any:
    df = pd.DataFrame(history, columns=['caller', 'callee'])
    G = nx.from_pandas_edgelist(df, 'caller', 'callee')
    return G

def graph_to_json(G: Any, json_location) -> None:
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(json_location), exist_ok=True)
    
    data = nx.node_link_data(G)
    with open(json_location, 'w') as f:
        json.dump(data, f)

def history_to_csv(history, location):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(location), exist_ok=True)
    
    with open(location, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['caller', 'callee'])
        for item in history:
            csv_writer.writerow(item)


def read_graph_from_json(json_location):
    with open(json_location, 'r') as f:
        data = json.load(f)
    G = nx.node_link_graph(data)
    return G

def df_to_csv(df, location):
    df[['caller', 'callee']].to_csv(location, index=False)

def convert_tuples(tuples_list):
    # Flatten the list of tuples
    flat_list = [item for sublist in tuples_list for item in sublist]
    
    # Create a dictionary to map unique numbers to new numbers
    unique_numbers = sorted(set(flat_list))
    number_map = {num: i+1 for i, num in enumerate(unique_numbers)}

    # Convert the tuples using the map
    converted_tuples = [(number_map[num1], number_map[num2]) for num1, num2 in tuples_list]
    
    return converted_tuples

def dynamic_metrics_to_csv(result: History2VecResult, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['c', 'g', 'gamma', 'h', 'nc', 'no', 'oc', 'oo', 'r', 'y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'c': result.c,
            'g': result.g,
            'gamma': result.gamma,
            'h': result.h,
            'nc': result.nc,
            'no': result.no,
            'oc': result.oc,
            'oo': result.oo,
            'r': result.r,
            'y': result.y,
        })

def metrics_to_csv(metrics: Metrics, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['global_clustering_coefficient',
                      'average_path_length',
                        'average_degree',
                        'network_diameter',
                        'average_degree_connectivity',
                        'average_neighbor_degree',
                        'local_efficiency',
                        'global_efficiency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'global_clustering_coefficient': metrics.global_cluster_coefficient,
            'average_path_length': metrics.average_path_length,
            'average_degree': metrics.average_degree,
            'network_diameter': metrics.network_diameter,
            'average_degree_connectivity': metrics.average_degree_connectivity,
            'average_neighbor_degree': metrics.average_neighbor_degree,
            'local_efficiency': metrics.local_efficiency,
            'global_efficiency': metrics.global_efficiency
        })

def convert_tuples(tuples_list):
    # Flatten the list of tuples
    flat_list = [item for sublist in tuples_list for item in sublist]
    
    # Create a dictionary to map unique numbers to new numbers
    unique_numbers = sorted(set(flat_list))
    number_map = {num: i+1 for i, num in enumerate(unique_numbers)}

    # Convert the tuples using the map
    converted_tuples = [(number_map[num1], number_map[num2]) for num1, num2 in tuples_list]
    
    return converted_tuples