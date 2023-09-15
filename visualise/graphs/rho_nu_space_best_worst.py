import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.colors as mcolors

types = {"nctf": "NCTF", "ttf": "TTF"}

for type, name in types.items():
    # Load the CSV data into DataFrames
    explorative_df = pd.read_csv("../../full_search/results/explorative/output.csv")

    best_ttf = {
        "rho": explorative_df.sort_values(by='ttf_mean').head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='ttf_mean').head(1)["nu"].iloc[0],
        "nctf": explorative_df.sort_values(by='ttf_mean').head(1)["nctf_mean"].iloc[0],
        "ttf": explorative_df.sort_values(by='ttf_mean').head(1)["ttf_mean"].iloc[0]
    }

    best_nctf = {
        "rho": explorative_df.sort_values(by='nctf_mean').head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='nctf_mean').head(1)["nu"].iloc[0],
        "nctf": explorative_df.sort_values(by='nctf_mean').head(1)["nctf_mean"].iloc[0],
        "ttf": explorative_df.sort_values(by='nctf_mean').head(1)["ttf_mean"].iloc[0]
    }

    worst_ttf = {
        "rho": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["nu"].iloc[0],
        "nctf": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
        "ttf": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]
    }

    worst_nctf = {
        "rho": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
        "nctf": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
        "ttf": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]
    }

    param_dict = {
        "best_ttf": best_ttf,
        "best_nctf": best_nctf,
        "worst_ttf": worst_ttf,
        "worst_nctf": worst_nctf
    }

# Define color maps for color coding based on the value
cmap = plt.get_cmap('viridis')

for type, name in types.items():
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if type == "nctf":
        best, worst = best_nctf, worst_nctf
        c_norm = mcolors.Normalize(vmin=explorative_df['nctf_mean'].min(), vmax=explorative_df['nctf_mean'].max())
    else:
        best, worst = best_ttf, worst_ttf
        c_norm = mcolors.Normalize(vmin=explorative_df['ttf_mean'].min(), vmax=explorative_df['ttf_mean'].max())

    # Plot best and worst points
    ax.scatter(best['rho'], best['nu'], color=cmap(c_norm(best[type])), s=100, label=r'Best ${}$'.format(type))
    ax.scatter(worst['rho'], worst['nu'], color=cmap(c_norm(worst[type])), s=100, label=r'Worst ${}$'.format(type))
    
    ax.set_xlim(0.5, 5.5)  # Adjusted left and right space
    ax.set_ylim(1, 30)
    
    # Adjust x-axis to only have integer ticks
    ax.set_xticks(np.arange(1, 6, 1))
    
    ax.set_title(name)
    ax.set_xlabel('$\\rho$')
    ax.set_ylabel('$\\nu$')
    ax.legend()

    # Create a "mappable" object for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=c_norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label(name)

    # Save the figure
    fig.tight_layout()  # Ensures that all elements of the plot fit within the figure boundaries
    
    # Save the figure
    fig.savefig(f"../results/rho_nu_space_{type}.png")