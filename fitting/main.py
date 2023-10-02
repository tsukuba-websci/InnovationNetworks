import sys
sys.path.append("..")

from argparse import ArgumentParser
from typing import Dict, cast

import pandas as pd
from history2bd.main import History2BD

from lib.history2vec import History2VecResult
from lib.julia_initializer import JuliaInitializer
from qd import QualityDiversitySearch

if __name__ == "__main__":
    # setup args
    arg_parser = ArgumentParser(description="Fitting a model using QD for a specific target.... Need a given file in /data/<target>.csv.")
    arg_parser.add_argument(
        "target_name",
        type=str,
        choices=["twitter", "aps", "ideastorm", "netbiz"],
        help="Target Data",
    )
    arg_parser.add_argument("dim", type=int, choices=[64, 128, 256], help="dimensionality of embedding in graph2vec")
    arg_parser.add_argument("cells", type=int, help="number of cells in archive")
    arg_parser.add_argument("rho", type=int, nargs="?", default=None, help="rho")
    arg_parser.add_argument("nu", type=int, nargs="?", default=None, help="nu")
    arg_parser.add_argument("s", type=str, nargs="?", default=None, choices=["SSW", "WSW"], help="strategy")
    args = arg_parser.parse_args()

    target_name: str = args.target_name
    dim: int = args.dim
    cells: int = args.cells

    # load models about the axes of QD
    history2bd = History2BD(
        graph2vec_model_path=f"./models/dim{dim}/graph2vec.pkl",
        standardize_model_path=f"./models/dim{dim}/standardize.pkl",
    )

    target_csv = f"../data/metrics/{target_name}.csv"
    df = cast(Dict[str, float], pd.read_csv(target_csv).iloc[0].to_dict())
    target = History2VecResult(**df)
    num_generations = 200

    # Set Up Julia
    jl_main, thread_num = JuliaInitializer().initialize()

    # run QD
    qds = QualityDiversitySearch(
        target_name=target_name,
        target=target,
        history2bd=history2bd,
        iteration_num=num_generations,
        thread_num=thread_num,
        jl_main=jl_main,
        dim=dim,
        result_dir_path=f"results/{target_name}",
        cells=cells,
    )
    qds.run()