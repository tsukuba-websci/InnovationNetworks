import numpy as np
import sys
sys.path.append("../utils")
from utils import *
import networkx as nx
import random

l = 2
k = 1
L = [k for _ in range(l)]

G = history_to_graph("../data/output/history/history_simulation_1.csv")
N = G.number_of_nodes()

knowledge = np.zeros((N,l))

################################################
################################################
################################################

# Setup
selected_indices = np.random.choice(N, l, replace=False)
selected_rows = knowledge[selected_indices]

for idx, row_idx in enumerate(selected_indices):
    knowledge[row_idx][idx] = k

################################################
################################################
################################################





################################################
################################################
################################################

steps = 1

for _ in range(steps):
    selected_nodes = set()
    for node in G.nodes():
        # Exclude nodes that have already been selected
        available_neighbors = [n for n in G.neighbors(node) if n not in selected_nodes]
        
        if len(available_neighbors) > 1:
            interaction_partner = random.choice(available_neighbors)
            communication_dimension = random.randint(0, l-1)

        else:
            interaction_partner = None  # Or handle this situation as required

        # Add the current node to the set of selected nodes
        selected_nodes.add(node)






################################################
################################################
################################################
        
