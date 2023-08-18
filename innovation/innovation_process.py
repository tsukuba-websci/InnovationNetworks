import numpy as np
import sys
sys.path.append("../utils")
from utils import *
import networkx as nx
import random

l = 2
k = 1
dv = 0.5
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

print(knowledge)

################################################
################################################
################################################





################################################
################################################
################################################

steps = 1

class BreakAllLoops(Exception):
    pass

history = []
try:
    for _ in range(steps):
        selected_nodes = set()
        step_history = []

        for caller in G.nodes():
            available_neighbors = [n for n in G.neighbors(caller) if n not in selected_nodes]
            
            if len(available_neighbors) > 1:
                callee = random.choice(available_neighbors)
                communication_dimension = random.randint(0, l-1)

                caller_knowledge = knowledge[caller-1][communication_dimension]
                callee_knowledge = knowledge[callee-1][communication_dimension]
                
                if caller_knowledge < callee_knowledge:
                    knowledge[caller-1][communication_dimension] += dv
                else:
                    knowledge[callee-1][communication_dimension] += dv

                step_history.append([caller,callee])
                selected_nodes.update([caller, callee])

                # Check if every column in any row of knowledge is k or greater
                if all(item >= k for item in knowledge[caller-1]) or all(item >= k for item in knowledge[callee-1]):
                    history.append(step_history)
                    raise BreakAllLoops
            
            else:
                # Handling for no available neighbors
                pass
        history.append(step_history)

except BreakAllLoops:
    print("Breaking out of loops as all columns in some row of knowledge have reached or exceeded the threshold.")

################################################
################################################
################################################
        
print(knowledge)
print(history)