import os
import pickle
import time
import networkx as nx
import sys
sys.path.append("..")
from multiprocessing import Pool
from typing import Any, List, Union
from lib.run_innovation_process import *
from lib.utils import *
from lib.graph2metrics import Graph2Metrics
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List
import os

import numpy as np
import pandas as pd
import ribs.emitters as emitters
import ribs.schedulers as schedulers
from history2bd.main import History2BD
from ribs.archives import CVTArchive
from tqdm import tqdm

@dataclass
class Params:
    rho: float
    nu: float
    s: str
    gamma: float
    eta: float
    steps: int
    nodes: int = 100
    threads: int = 1

class QualityDiversitySearch:
    k: int
    l: int
    dv: int
    history2bd: History2BD
    thread_num: int = 8
    jl_main: Any =  None
    result_dir_path: str
    archives_dir_path: str
    iteration_num: int
    target: str

    def __init__(
        self,
        k: int,
        l: int,
        dv: int,
        history2bd: History2BD,
        iteration_num: int,
        thread_num: int,
        jl_main: Any,
        target: str,
        dim: int,
        cells: int,
        result_dir_path: str,
    ) -> None:
        self.k = k
        self.l = l
        self.dv = dv
        self.history2bd = history2bd
        self.iteration_num = iteration_num
        self.thread_num = thread_num
        self.jl_main = jl_main
        self.target = target
        self.dim = dim
        self.cells = cells
        self.result_dir_path = result_dir_path
        self.archives_dir_path = f"{self.result_dir_path}/archives"

        os.makedirs(self.archives_dir_path, exist_ok=True)

    def prepare_archive(self) -> CVTArchive:
        archive: Union[CVTArchive, None] = None
        if os.path.exists(f"{self.result_dir_path}/archive.pkl"):
            with open(f"{self.result_dir_path}/archive.pkl", "rb") as f:
                archive = pickle.load(f)
        else:
            archive = CVTArchive(
                solution_dim=2,
                cells=self.cells,
                ranges=[(-5, 5) for _ in range(self.dim)],
            )
        assert archive is not None, "archive should not be None!"
        return archive

    def save_archive(self, archive: CVTArchive, iter: int) -> pd.DataFrame:
        # save latest archive
        with open(f"{self.result_dir_path}/archive.pkl", "wb") as file:
            pickle.dump(archive, file)

        # save archive as csv
        df = archive.as_pandas()
        df.rename(
            columns={
                "solution_0": "rho",
                "solution_1": "nu"
            },
            inplace=True,
        )
        df["objective"] = -df["objective"]
        df.rename(columns={"objective": "NCTF"}, inplace=True)
        df = df[["rho", "nu", "NCTF"]].sort_values(by="NCTF", ascending=True)
        df.to_csv(f"{self.archives_dir_path}/{iter:0>8}.csv", index=False)
        return df

    def set_params_list(self, sols: List[np.ndarray]) -> List[Params]:
        rhos: List[int] = list(map(lambda sol: sol[0].item(), sols))
        nus: List[int] = list(map(lambda sol: sol[1].item(), sols))
        s: List[str] = ["asw" for _ in range(len(rhos))]
        gammas: List[float] = [0.1 for _ in range(len(rhos))]
        etas: List[float] = [0.9 for _ in range(len(rhos))]
        steps: List[int] = [9999999 for _ in range(len(rhos))]
        nodes: List[int] = [100 for _ in range(len(rhos))]
        threads: List[int] = [self.thread_num for _ in range(len(rhos))]

        params_list = list(map(
            lambda t: Params(*t),
            zip(rhos, nus, s, gammas, etas, steps, nodes, threads),
        ))
        return params_list

    def print_status(self, archive: CVTArchive, iter: int, start_time: time) -> None:
        elapsed_time = time.time() - start_time
        print(f"> {iter} iters completed after {elapsed_time:.2f} s")
        print(f"  - Archive Size: {len(archive)}")
        assert archive.stats is not None, "archive.stats is None!"
        print(f"  - Max Score: {archive.stats.obj_max}")

    def run(self):
        archive: Union[CVTArchive, None] = self.prepare_archive()

        already = 0
        if os.path.exists(self.archives_dir_path):
            already = len(os.listdir(self.archives_dir_path))

        initial_model = np.zeros(2)
        bounds = [
            (1, 10),
            (1, 10),
        ]
        emitters_ = [
            emitters.EvolutionStrategyEmitter(
                archive=archive,
                x0=initial_model,
                sigma0=1.0,
                bounds=bounds,
                ranker="2imp",
            )
            for _ in range(5)
        ]
        optimizer = schedulers.Scheduler(archive, emitters_)

        start_time = time.time()

        for iter in tqdm(range(already, self.iteration_num), desc=f"Innovation Search: {self.target}"):
            # Request models from the scheduler
            sols = optimizer.ask()

            params_list = self.set_params_list(sols)

            histories = self.jl_main.parallel_run_waves_model(params_list)

            bcs = self.history2bd.run(histories)
            objs = []

            for history in histories:
                renumbered_history = convert_tuples(history)
                G = nx.Graph()
                G.add_edges_from(renumbered_history)
                NCTF_list = []
                TTF_list = []
                for i in range(100):
                    NCTF, TTF, failed = run_innovation_process(G, self.l, self.k, self.dv, 200)
                    NCTF_list.append(NCTF)
                    TTF_list.append(TTF)
                
                average_NCTF = sum(NCTF_list)/len(NCTF_list)
                average_TTF = sum(TTF_list)/len(TTF_list)

                if self.target == "min_NCTF":
                    obj: np.float64 = average_NCTF
                    objs.append(-obj)
                elif self.target == "max_NCTF":
                    obj: np.float64 = average_NCTF
                    objs.append(obj)
                elif self.target == "min_TTF":
                    obj: np.float64 = average_TTF
                    objs.append(-obj)
                elif self.target == "max_TTF":
                    obj: np.float64 = average_TTF
                    objs.append(obj)

            # Send the results back to the scheduler
            optimizer.tell(objs, bcs)

            # save archive
            df = self.save_archive(archive, iter)

            if iter % 25 == 0:
                self.print_status(archive, iter, start_time)

            # Filter the DataFrame where innovation failed
            # filtered_df = df[df['NCTF'] > -9999]
            # filtered_df.head(30).to_csv(f"{self.result_dir_path}/best.csv", index=False)
            df.head(30).to_csv(f"{self.result_dir_path}/best.csv", index=False)

    def analyse(self):
        best_parameter_set = pd.read_csv(f"{self.result_dir_path}/best.csv")

        for index, row in best_parameter_set.iterrows():
            history = self.jl_main.parallel_run_waves_model([Params(rho=row['rho'], nu=row['nu'], s="asw", gamma=0.1, eta=0.9, steps=1000000, nodes=100, threads=1)])[0]

            history_to_csv(history=history, location=f"{self.result_dir_path}/history/{index}.csv")
            graph = history_to_graph(csv_location=f"{self.result_dir_path}/history/{index}.csv")
            graph_to_json(graph, f"../web_server/src/data/{self.target}{index}.json")

            metrics = Graph2Metrics().graph2metrics(graph=graph)
            metrics_to_csv(metrics, f"{self.result_dir_path}/metrics/{index}.csv")
