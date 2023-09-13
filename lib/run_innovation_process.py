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

def run_innovation_process_parallel(args):
    G, l, k, dv, num_iterations = args
    return run_innovation_process(G, l, k, dv, num_iterations)

def run_innovation_process(G, l, k, dv, steps):
    # Setup
    L = [k for _ in range(l)]
    N = G.number_of_nodes()
    knowledge = np.zeros((N, l))

    history = []
    total_knowledge_history = []  # List to store total knowledge at every time step
    std_deviation_history = []  # List to store the standard deviation of the total knowledge of each node

    # Run Innovation Simulation
    try:
        if N > l:
            # distribute initial knowledge
            selected_indices = np.random.choice(N, l, replace=False)
            for idx, row_idx in enumerate(selected_indices):
                knowledge[row_idx][idx] = k
        else:
            raise NotEnoughNodes
        
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
                        raise InnovationAchieved
                
                else:
                    # Handling for no available neighbors
                    pass

            # Calculation of total knowledge at this time step
            total_knowledge_history.append(np.sum(knowledge))
            
            # Calculation of standard deviation of the total knowledge of each node at this time step
            node_total_knowledge_history = np.sum(knowledge, axis=1)
            std_dev = np.std(node_total_knowledge_history)
            std_deviation_history.append(std_dev)

            history.append(step_history)

        # Return statements with total_knowledge_history and std_deviation_history lists
        return 999999999, 999999999, True, total_knowledge_history, std_deviation_history

    except InnovationAchieved:
        NCTF = len([item for sublist in history for item in sublist])
        TTF = len(history)
        return NCTF, TTF, False, total_knowledge_history, std_deviation_history
    
    except NotEnoughNodes:
        return 999999999, 999999999, True, total_knowledge_history, std_deviation_history
