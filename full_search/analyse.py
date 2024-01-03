import sys
sys.path.append("..")
import pandas as pd
from lib.julia_initializer import JuliaInitializer
import os
import csv
from full_search import Params, InnovationType
from multiprocessing import Pool
from lib.run_innovation_process import *
from lib.utils import *
from typing import List
from lib.graph2metrics import Graph2Metrics

def main():
    innovation_types = {
        "explorative": InnovationType(1, 20, 1),
        "exploitative": InnovationType(20, 2, 1)
    }

    explorative_df = pd.read_csv("results/explorative/output.csv")
    exploitative_df = pd.read_csv("results/exploitative/output.csv")  # Load exploitative results

    best_ttf_explorative = {
        "rho": explorative_df.sort_values(by='ttf_mean').head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='ttf_mean').head(1)["nu"].iloc[0]
    }

    best_nctf_explorative = {
        "rho": explorative_df.sort_values(by='nctf_mean').head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='nctf_mean').head(1)["nu"].iloc[0]
    }

    worst_ttf_explorative = {
        "rho": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["nu"].iloc[0]
    }

    worst_nctf_explorative = {
        "rho": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0]
    }

    best_ttf_exploitative = {
        "rho": exploitative_df.sort_values(by='ttf_mean').head(1)["rho"].iloc[0],
        "nu": exploitative_df.sort_values(by='ttf_mean').head(1)["nu"].iloc[0]
    }

    best_nctf_exploitative = {
        "rho": exploitative_df.sort_values(by='nctf_mean').head(1)["rho"].iloc[0],
        "nu": exploitative_df.sort_values(by='nctf_mean').head(1)["nu"].iloc[0]
    }

    worst_ttf_exploitative = {
        "rho": exploitative_df.sort_values(by='ttf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": exploitative_df.sort_values(by='ttf_mean', ascending=False).head(1)["nu"].iloc[0]
    }

    worst_nctf_exploitative = {
        "rho": exploitative_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": exploitative_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0]
    }

    param_dict = {
        "best_ttf_explorative": best_ttf_explorative,
        "best_nctf_explorative": best_nctf_explorative,
        "worst_ttf_explorative": worst_ttf_explorative,
        "worst_nctf_explorative": worst_nctf_explorative,
        "best_ttf_exploitative": best_ttf_exploitative,
        "best_nctf_exploitative": best_nctf_exploitative,
        "worst_ttf_exploitative": worst_ttf_exploitative,
        "worst_nctf_exploitative": worst_nctf_exploitative
    }

    print(param_dict)

    s = "asw"
    zeta = 0.5
    eta = 0.5
    steps = 1000000
    nodes = 100

    num_networks = 100
    innovation_simulations_per_network = 1000

    # Run the model for the best worst solutions for both explorative and exploitative
    for entry, param_set in param_dict.items():
        rho = param_set["rho"]
        nu = param_set["nu"]

        best_worst = entry.split('_')[0]  # ex. best, worst
        innovation_measure = entry.split('_')[1]  # ex. ttf, nctf
        type_key = entry.split('_')[2]  # ex. explorative, exploitative
        innovation_type = innovation_types[type_key]

        print(f"Running for {type_key} with rho={rho} and nu={nu}")

        save_path = f"results/{type_key}"  # Corrected folder name
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        with open(f"{save_path}/{entry}.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write header
            csv_writer.writerow(["nctf", "ttf", "total_knowledge_history", "standard_deviation_history", "rho", "nu"])

            jl_main, thread_num = JuliaInitializer().initialize()

            # Generate Networks
            params = Params(rho=rho, nu=nu, s=s, zeta=zeta, eta=eta, steps=steps, nodes=nodes)

            params_list: List[Params] = [params for _ in range(num_networks)]
            network_histories = jl_main.parallel_run_waves_model(params_list)

            parsed_networks_histories = [convert_tuples(network_history_raw) for network_history_raw in network_histories]
            graphs = [history_object_to_graph(history=network_history_parsed) for network_history_parsed in parsed_networks_histories]

            output_directory = "data/output/graph"
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            counter = 0
            for graph in graphs:
                graph_to_json(graph, f"data/output/graph/{type}_{counter}.json")
                counter += 1

            metrics = [Graph2Metrics().graph2metrics(graph=graph) for graph in graphs]

            global_cluster_coefficients = [metric.global_cluster_coefficient for metric in metrics]
            average_global_cluster_coefficient = sum(global_cluster_coefficients) / len(global_cluster_coefficients)

            average_path_lengths = [metric.average_path_length for metric in metrics]
            average_average_path_length = sum(average_path_lengths) / len(average_path_lengths)

            average_degree = [metric.average_degree for metric in metrics]
            average_average_degree = sum(average_degree) / len(average_degree)

            network_diameter = [metric.network_diameter for metric in metrics]
            average_network_diameter = sum(network_diameter) / len(network_diameter)

            network_density = [metric.network_density for metric in metrics]
            average_network_density = sum(network_density) / len(network_density)

            # Save Metrics
            metrics_dir = f"{save_path}/metrics"
            if not os.path.exists(metrics_dir):
                os.makedirs(metrics_dir)

            with open(f"{metrics_dir}/{entry}_metrics.csv", 'w', newline='') as metrics_csvfile:
                csv_metrics_writer = csv.writer(metrics_csvfile)

                # Write header
                csv_metrics_writer.writerow(["rho", "nu", "average_global_cluster_coefficient", "average_average_path_length",
                                                "average_average_degree", "average_network_diameter", "average_network_density"])


            # Run Innovation Simulations
            args = [(G, innovation_types[type.split('_')[2]].l, innovation_types[type.split('_')[2]].k,
                     innovation_types[type.split('_')[2]].dv, 200)
                    for G in graphs for _ in range(innovation_simulations_per_network)]

            with Pool(processes=int(os.environ.get("JULIA_NUM_THREADS", 4))) as pool:
                results = pool.map(run_innovation_process_parallel, args)

            print("processing results")

            for result in results:
                nctf = result[0]
                ttf = result[1]
                failed = result[2]
                total_knowledge_history = result[3]
                std_deviation_history = result[4]

                # Convert the histories to string format
                total_knowledge_str = '|'.join(map(str, total_knowledge_history))
                std_deviation_str = '|'.join(map(str, std_deviation_history))

                # Write the NCTF, total_knowledge_str, and std_deviation_str to csv file
                csv_writer.writerow([nctf, ttf, total_knowledge_str, std_deviation_str, rho, nu])

if __name__ == "__main__":
    main()
