import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

labels = np.array(cols)
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))  # Add the first angle to the end to close the plot

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})

# Plot data from the four CSV files
for key, values in data.items():
    values_to_plot = np.concatenate((values, [values[0]]))  # Close the plot by appending the first value to the end of data vector
    ax.plot(angles, values_to_plot, 'o-', linewidth=2, label=key)  # Add a label corresponding to dataframe's name
    ax.fill(angles, values_to_plot, alpha=0.25)

ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)  # -1 to remove the last repeated angle
ax.set_title("Radar Plot of Network Measures")
ax.grid(True)
ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.1))  # Place the legend outside of the plot

plt.savefig('../results/metrics_radar.png', dpi=300)  # Save the plot as an image
