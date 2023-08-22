import os

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

plt.rcParams["font.size"] = 18


def archives2df(df: pd.DataFrame, df_min: pd.DataFrame):
    # Add the distance of all individuals to df and the distance of the best individual in each generation to df_min

    basedir = f"../qd/results/NCTF/archives"
    files = sorted(os.listdir(basedir))

    for gen, file in enumerate(files):
        _df = pd.read_csv(f"{basedir}/{file}")
        _df["generation"] = gen
        _df = _df[["generation", "distance"]]
        df = pd.concat([df, _df])

        _df_min = _df.head(1)
        df_min = pd.concat([df_min, _df_min])
    return df, df_min


def plot_data(data: dict, data_min: dict, ymax: float, file_name: str, palette: list) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    # 全個体の距離の平均と標準偏差
    sns.lineplot(
        data=data['qd'],
        x="generation",
        y="distance",
        legend=False,
        ax=ax,
        alpha=0.3,
        palette=palette,
    )
    # 各世代の最良個体の距離
    sns.lineplot(
        data=data_min['qd'],
        x="generation",
        y="distance",
        legend=False,
        ax=ax,
        linestyle="--",
        palette=palette,
    )
    plt.xlabel("Generation", fontsize=24)
    plt.ylabel("d", fontsize=24)
    plt.ylim(0, ymax)
    plt.tight_layout()
    plt.savefig(f"results/timeline/qd/{file_name}.png", dpi=300)
    plt.close()


def plot_timeline(my_color: dict) -> None:
    """
    Plot the learning curve of QD
    Plot the mean and standard deviation of the distances of all individuals and the distance of the best individual in each generation.
    """
    algorithm = "qd"
    data = {}
    data_min = {}
    ymax = 0
    data_alg = pd.DataFrame()
    data_alg_min = pd.DataFrame()


    df, df_min = archives2df(pd.DataFrame(), pd.DataFrame())
    data_alg = pd.concat([data_alg, df])
    data_alg_min = pd.concat([data_alg_min, df_min])
    ymax = max(ymax, df.groupby("generation")["distance"].mean().max())
    data[algorithm] = data_alg
    data_min[algorithm] = data_alg_min

    plot_data(data, data_min, ymax, "test", [my_color["dark_red"]])
