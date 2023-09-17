import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.colors as mcolors

types = {"nctf_mean": "NCTF", "ttf_mean": "TTF"}

explorative_df = pd.read_csv("../../full_search/results/explorative/output.csv")

# Preparing data for heatmap (using pivot)
for type, name in types.items():
    data_pivot = explorative_df.pivot(index='nu', columns='rho', values=type)
    
    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(data_pivot, cmap='viridis', ax=ax, cbar_kws={'label': name})

    # Settings for aesthetics
    ax.set_title(name, fontsize=16)
    ax.set_xlabel('$\\rho$', fontsize=14)
    ax.set_ylabel('$\\nu$', fontsize=14)
    ax.invert_yaxis()  # to match with scatter plot y-axis direction

    # Save the figure
    fig.tight_layout()
    fig.savefig(f"../results/rho_nu_space_grid_{type}.png", dpi=300)
