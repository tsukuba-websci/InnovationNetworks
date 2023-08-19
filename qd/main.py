from argparse import ArgumentParser
import sys
sys.path.append("..")
import pandas as pd
from history2bd.main import History2BD

from lib.julia_initializer import JuliaInitializer
from qd import QualityDiversitySearch

if __name__ == "__main__":
    # setup args
    arg_parser = ArgumentParser(description="特定のターゲットに対してQDを使ってモデルをフィッティングする。../data/<target>.csvに所定のファイルが必要。")
    arg_parser.add_argument("dim", type=int, choices=[64, 128, 256], help="dimensionality of embedding in graph2vec")
    arg_parser.add_argument("cells", type=int, help="number of cells in archive")
    args = arg_parser.parse_args()

    dim: int = args.dim
    cells: int = args.cells

    k = 2
    l = 2
    dv = 1

    # load models about the axes of QD
    history2bd = History2BD(
        graph2vec_model_path=f"./models/dim{dim}/graph2vec.pkl",
        standardize_model_path=f"./models/dim{dim}/standardize.pkl",
    )

    num_generations = 2

    # Set Up Julia
    jl_main, thread_num = JuliaInitializer().initialize()

    print(f"thread_number: {thread_num}")

    # run QD
    qds = QualityDiversitySearch(
        history2bd=history2bd,
        iteration_num=num_generations,
        thread_num=thread_num,
        jl_main=jl_main,
        dim=dim,
        result_dir_path=f"results/NCTF/",
        cells=cells,
        k=k,
        l=l,
        dv=dv
    )
    print("Starting QD")
    qds.run()
