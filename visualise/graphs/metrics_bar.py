import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

my_color = {
    "red": "#FC8484",
    "dark_red": "#FA5050",
    "light_blue": "#94C4E0",
    "light_green": "#9CDAA0",
    "dark_blue": "#76ABCB",
    "dark_green": "#51BD56",
    "black": "#505050",
    "purple": "#CBA6DD",
    "yellow": "#FFE959",
    "yellow_green": "#C1FF87",
}

file_location = "../../full_search/results/explorative/best_worst/"

best_nctf = pd.read_csv(f"{file_location}/best_nctf/metrics.csv")
worst_nctf = pd.read_csv(f"{file_location}/worst_nctf/metrics.csv")
best_ttf = pd.read_csv(f"{file_location}/best_ttf/metrics.csv")
worst_ttf = pd.read_csv(f"{file_location}/worst_ttf/metrics.csv")

cols = [
    "average_global_cluster_coefficient",
    "average_average_path_length",
    "average_average_degree",
    "average_network_diameter"
]

# Extract the values from each dataframe
data = {
    'Best NCTF': best_nctf[cols].iloc[0].values,
    'Worst NCTF': worst_nctf[cols].iloc[0].values,
    'Best TTF': best_ttf[cols].iloc[0].values,
    'Worst TTF': worst_ttf[cols].iloc[0].values
}

bar_width = 0.35
index = np.arange(2)  # We have 2 groups: NCTF and TTF

titles_readable = {
    "average_global_cluster_coefficient": "Average Global Cluster Coefficient",
    "average_average_path_length": "Average Path Length",
    "average_average_degree": "Average Degree",
    "average_network_diameter": "Network Diameter"
}

# Iterate over each metric
for col, title in zip(cols, titles_readable.values()):
    fig, ax = plt.subplots(figsize=(6, 5))
    
    ax.bar(index, [data['Best NCTF'][cols.index(col)], data['Best TTF'][cols.index(col)]], bar_width, label="Best", color=my_color["dark_green"])
    ax.bar(index + bar_width, [data['Worst NCTF'][cols.index(col)], data['Worst TTF'][cols.index(col)]], bar_width, label="Worst", color=my_color["dark_red"])

    ax.set_ylabel(title)
    ax.set_title(title)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(['NCTF', 'TTF'])
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'../results/metrics_{col}.png', dpi=300)
    plt.close(fig)
