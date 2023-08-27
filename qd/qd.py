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
from lib.history2vec import History2Vec, History2VecResult
from lib.graph2metrics import Graph2Metrics, Metrics

import os

import numpy as np
import pandas as pd
import ribs.emitters as emitters
import ribs.schedulers as schedulers
from history2bd.main import History2BD
from ribs.archives import CVTArchive
from tqdm import tqdm

from lib.run_model import Params, run_model

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
                solution_dim=4,
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
                "solution_1": "nu",
                "solution_2": "recentness",
                "solution_3": "frequency",
            },
            inplace=True,
        )
        df["objective"] = -df["objective"]
        df.rename(columns={"objective": "distance"}, inplace=True)
        df = df[["rho", "nu", "recentness", "frequency", "distance"]].sort_values(by="distance", ascending=True)
        df.to_csv(f"{self.archives_dir_path}/{iter:0>8}.csv", index=False)
        return df

    def set_params_list(self, sols: List[np.ndarray]) -> List[Params]:
        rhos: List[float] = list(map(lambda sol: sol[0].item(), sols))
        nus: List[float] = list(map(lambda sol: sol[1].item(), sols))
        recentnesses: List[float] = list(map(lambda sol: sol[2].item(), sols))
        frequency: List[float] = list(map(lambda sol: sol[3].item(), sols))
        steps = [20000 for _ in range(len(rhos))]

        params_list = map(
            lambda t: Params(*t),
            zip(rhos, nus, recentnesses, frequency, steps),
        )
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

        initial_model = np.zeros(4)
        bounds = [
            (2, 30),  # 1 <= rho <= 20
            (2, 30),  # 1 <= nu <= 20
            (-1, 1),  # -1 <= recentness <= 1
            (-1, 1),  # -1 <= frequency <= 1
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

            # Evaluate the models and record the objectives and measuress.
            with Pool(self.thread_num) as pool:
                histories = pool.map(run_model, params_list)

            bcs = self.history2bd.run(histories)
            objs = []

            for history in histories:
                renumbered_history = convert_tuples(history)
                G = nx.Graph()
                G.add_edges_from(renumbered_history)
                NCTF_list = []
                TTF_list = []
                failed_list = []
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

            # save best result as csv
            df.head(30).to_csv(f"{self.result_dir_path}/best.csv", index=False)

    def analyse(self):
        best_parameter_set = pd.read_csv(f"{self.result_dir_path}/best.csv")

        for index, row in best_parameter_set.iterrows():
            history = run_model(Params(rho=row['rho'], nu=row['nu'], recentness=row['recentness'], frequency=row['frequency'], steps=20000))

            history_to_csv(history=history, location=f"{self.result_dir_path}/history/{index}.csv")
            graph = history_to_graph(csv_location=f"{self.result_dir_path}/history/{index}.csv")
            graph_to_json(graph, f"../web_server/src/data/{self.target}{index}.json")

            metrics = Graph2Metrics().graph2metrics(graph=graph)
            metrics_to_csv(metrics, f"{self.result_dir_path}/metrics/{index}.csv")