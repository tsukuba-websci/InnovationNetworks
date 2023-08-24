import numpy as np
import sys
sys.path.append("../utils")
from utils import *
import networkx as nx
import random

class InnovationAchieved(Exception):
    pass

class NotEnoughNodes(Exception):
    pass


def run_innovation_process(G, l, k, dv, steps):

    # Setup
    L = [k for _ in range(l)]
    N = G.number_of_nodes()
    knowledge = np.zeros((N,l))

    history = []

    # Run Innovation Simulation
    try:
        if N>l:
            # distribute initial knowledge
            selected_indices = np.random.choice(N, l, replace=False)
            for idx, row_idx in enumerate(selected_indices):
                knowledge[row_idx][idx] = k
        else:
            raise NotEnoughNodes

        for step in range(steps):
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
                        raise InnovationAchieved
                
                else:
                    # Handling for no available neighbors
                    pass
            history.append(step_history)

        # print(f"Innovation unsuccessful after {steps} steps.")
        return 999999, 999999, True


    except InnovationAchieved:
        # print(f"Innovation occured after {step+1} steps.")
        NCTF = len([item for sublist in history for item in sublist])
        TTF = len(history)
        return NCTF, TTF, False
    
    except NotEnoughNodes:
        # print(f"Not Enough Nodes")
        return 999999, 999999, True    