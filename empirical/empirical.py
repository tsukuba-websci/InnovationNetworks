import sys
sys.path.append("..")
from lib.run_innovation_process import *
from lib.utils import *
import csv
from dataclasses import dataclass
from typing import List
from multiprocessing import Pool
from lib.julia_initializer import JuliaInitializer

@dataclass
class Params:
    rho: float
    nu: float
    s: str
    zeta: float
    eta: float
    steps: int
    nodes: int = 100

class InnovationType:
    k: int
    l: int
    dv: int

    def __init__(self, k, l, dv):
        self.k = k
        self.l = l
        self.dv = dv

class Empirical:
    target: str
    params: Params
    innovation_type: InnovationType
    results_dir_path: str

    def __init__(
            self,
            target: str,
            innovation_type: InnovationType,
            results_dir_path: str,
            params: Params,
    ) -> None:
        self.target = target
        self.innovation_type = innovation_type
        self.results_dir_path = results_dir_path
        self.params = params
    
    def run(self):
        if not os.path.exists(self.results_dir_path):
            os.makedirs(self.results_dir_path)

        with open(f"{self.results_dir_path}/output.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["rho", "nu", "s", "zeta", "eta", "steps", "nodes", "nctf_mean", "ttf_mean"])
            
            jl_main, thread_num = JuliaInitializer().initialize()

            nctf_list = []
            ttf_list = []

            num_networks = 100
            innovation_simulations_per_network = 1000

            # Generate networks
            params_list: List[Params] = [self.params for _ in range(num_networks)]
            network_histories = jl_main.parallel_run_waves_model(params_list)
            parsed_networks_histories = [convert_tuples(network_history_raw) for network_history_raw in network_histories]
            graphs = [history_object_to_graph(history=network_history_parsed) for network_history_parsed in parsed_networks_histories]

            # Run Innovation Simulations
            args = [(G, self.innovation_type.l, self.innovation_type.k, self.innovation_type.dv, 200) 
                for G in graphs for _ in range(innovation_simulations_per_network)]

            with Pool(processes=int(os.environ.get("JULIA_NUM_THREADS", 4))) as pool:
                results = pool.map(run_innovation_process_parallel, args)
            
            for result in results:
                nctf = result[0]
                ttf = result[1]
                nctf_list.append(nctf)
                ttf_list.append(ttf)

            nctf_mean = sum(nctf_list) / len(nctf_list)
            ttf_mean = sum(ttf_list) / len(ttf_list)

            csv_writer.writerow([self.params.rho, self.params.nu, self.params.s, self.params.zeta, self.params.eta, self.params.steps, self.params.nodes, nctf_mean, ttf_mean])

            
