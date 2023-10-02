import sys
sys.path.append("..")
import os
from argparse import ArgumentParser

from lib.history2vec import History2VecResult
from lib.julia_initializer import JuliaInitializer
import pandas as pd
from collections import defaultdict


def df_to_metrics(df, metrics_location, interval_num, jl_main):
    user_mapping = defaultdict(lambda: len(user_mapping))
    history = [(user_mapping[caller], user_mapping[callee]) for caller, callee in df[['caller', 'callee']].values]

    if any(map(lambda row: row[0] == 0 or row[1] == 0, history)):
        history = list(map(lambda row: (row[0] + 1, row[1] + 1), history))

    nt = jl_main.history2vec(history, interval_num)

    result = History2VecResult(
        c=nt.c,
        g=nt.g,
        gamma=nt.gamma,
        h=nt.h,
        nc=nt.nc,
        no=nt.no,
        oc=nt.oc,
        oo=nt.oo,
        r=nt.r,
        y=nt.y,
    )

    results = pd.DataFrame([result._asdict()])
    results.to_csv(metrics_location, index=False)

if __name__ == "__main__":
    arg_parser = ArgumentParser(description="Calculate the 10 network metrics given a target.")
    arg_parser.add_argument(
        "target_name",
        type=str,
        choices=["twitter", "aps", "ideastorm", "netbiz"],
        help="Target Data",
    )

    target_name: str = arg_parser.parse_args().target_name

    # Set Up Julia
    jl_main, thread_num = JuliaInitializer().initialize()

    # Read in the processed csv:
    input = f"../data/networks/{target_name}/processed/{target_name}_processed.csv"
    output = f"../data/metrics/{target_name}.csv"

    # Check if the file exists
    if os.path.exists(input):
        # If the file exists, read it using pd.read_csv
        df = pd.read_csv(input)
        df_to_metrics(df, output, 1000, jl_main)
        print("Metrics calculated successfully.")
        # Now you can work with the DataFrame df
    else:
        print(f"The file {input} does not exist.")
