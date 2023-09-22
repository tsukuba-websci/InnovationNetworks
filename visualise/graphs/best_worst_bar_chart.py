import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy import stats

types = {"nctf": "NCTF", "ttf": "TTF"}

# Create a combined figure and axis array
fig, axes = plt.subplots(nrows=1, ncols=len(types), figsize=(12, 6))

# Loop through each type and its corresponding axis
for (type, name), ax in zip(types.items(), axes):

    if type == "nctf":
        other = "ttf"
    elif type == "ttf":
        other = "nctf"


    best_csv = f"../../full_search/results/explorative/best_worst/best_{type}.csv"
    worst_csv = f"../../full_search/results/explorative/best_worst/worst_{type}.csv"

    best_df = pd.read_csv(best_csv)
    worst_df = pd.read_csv(worst_csv)

    best_rho = best_df["rho"].iloc[0]
    worst_rho = worst_df["rho"].iloc[0]

    best_nu = best_df["nu"].iloc[0]
    worst_nu = worst_df["nu"].iloc[0]

    best_array = best_df[f"{type}"].to_numpy()
    worst_array = worst_df[f"{type}"].to_numpy()

    best_mean = np.mean(best_array)
    worst_mean = np.mean(worst_array)

    best_other_mean = np.mean(best_df[f"{other}"].to_numpy())
    worst_other_mean = np.mean(worst_df[f"{other}"].to_numpy())

    confidence = 0.95

    # Calculate the confidence interval for best_array
    n_best = len(best_array)
    std_err1 = np.std(best_array, ddof=1) / np.sqrt(n_best)
    ci_best = std_err1 * stats.t.ppf((1 + confidence) / 2, n_best - 1)

    # Calculate the confidence interval for worst_array
    n_worst = len(worst_array)
    std_err2 = np.std(worst_array, ddof=1) / np.sqrt(n_worst)
    ci_worst = std_err2 * stats.t.ppf((1 + confidence) / 2, n_worst - 1)

    ind = np.arange(1)
    width = 0.1

    print(f"Best {name} ({best_rho}, {best_nu}): {best_mean} ± {ci_best}, {other}: {best_other_mean}")
    print(f"Worst {name} ({worst_rho}, {worst_nu}): {worst_mean} ± {ci_worst}, {other}: {worst_other_mean}")

    # Bar plots for best and worst with error bars
    ax.bar(ind, best_mean, width, yerr=ci_best, label=r"Best {} ($\rho = {}$, $\nu = {}$)".format(name, best_rho, best_nu), alpha=0.7)
    ax.bar(ind + width, worst_mean, width, yerr=ci_worst, label=r"Worst {} ($\rho = {}$, $\nu = {}$)".format(name, worst_rho, worst_nu), alpha=0.7)

    # Set labels and title
    ax.set_xlabel('')
    ax.set_ylabel(f'{name}')
    ax.set_title(f'{name}')
    ax.set_xticks([])
    ax.legend()

# Set a main title for the combined plot
fig.suptitle('The Difference Between the Best and Worst Performing Innovation Networks')
plt.tight_layout()
plt.subplots_adjust(top=0.85)  # Adjust title position

# Save the combined plot
fig.savefig("../results/best_worst_combined.png", dpi=300)
