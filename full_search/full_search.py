import sys
sys.path.append("..")
from typing import Any
from lib.run_innovation_process import *
from lib.utils import *
import csv

class InnovationType:
    k: int
    l: int
    dv: int

    def __init__(self, k, l, dv):
        self.k = k
        self.l = l
        self.dv = dv

class FullSearch:
    innovation_type: InnovationType
    thread_num: int
    jl_main: Any = None
    results_dir_path: str
    target: str

    def __init__(
            self,
            innovation_type: InnovationType,
            thread_num: int,
            jl_main: Any,
            target: str,
            results_dir_path: str,
    ) -> None:
        self.innovation_type = innovation_type
        self.thread_num = thread_num
        self.jl_main = jl_main
        self.target = target
        self.results_dir_path = results_dir_path


    def run(self):
        if not os.path.exists(self.results_dir_path):
            os.makedirs(self.results_dir_path)

        with open(f"{self.results_dir_path}/output.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["rho", "nu", "s", "zeta", "eta", "steps", "nodes", "nctf_mean", "ttf_mean"])

            s = "asw"
            zeta = 0.5
            eta = 0.5
            steps = 1000000
            nodes = 100

            rho_min = 1
            rho_max = 2
            nu_min = 1
            nu_max = 2

            num_networks = 2
            innovation_simulations_per_network = 10

            for rho in range(rho_min, rho_max):
                for nu in range(nu_min, nu_max):
                    for _ in range(num_networks):
                        nctf_list = []
                        ttf_list = []
                        network_history_raw = self.jl_main.run_waves_model(rho, nu, s, zeta, eta, steps=steps, nodes=nodes)[0].history
                        network_history_parsed = convert_tuples(network_history_raw)
                        G = history_object_to_graph(history=network_history_parsed)
                        for _ in range(innovation_simulations_per_network):
                            nctf, ttf, failed, total_knowledge_history, std_deviation_history = run_innovation_process(G, self.innovation_type.l, self.innovation_type.k, self.innovation_type.k, 200)
                            nctf_list.append(nctf)
                            ttf_list.append(ttf)

                        nctf_mean = sum(nctf_list) / len(nctf_list)
                        ttf_mean = sum(ttf_list) / len(ttf_list)

                        csv_writer.writerow([rho, nu, s, zeta, eta, steps, nodes, nctf_mean, ttf_mean])
