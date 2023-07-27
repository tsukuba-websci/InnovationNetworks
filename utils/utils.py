import pandas as pd
from typing import Any
import matplotlib.pyplot as plt
import csv
import json
import pandas as pd
import networkx as nx
from typing import Any, NamedTuple

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

def graph_to_json(G: Any, json_location) -> None:
    data = nx.node_link_data(G)
    with open(json_location, 'w') as f:
        json.dump(data, f)

def history_to_csv(history, location):
    with open(location, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['caller', 'callee'])
        for item in history:
            csv_writer.writerow(item)
    pass

def df_to_csv(df, location):
    df[['caller', 'callee']].to_csv(location, index=False)
