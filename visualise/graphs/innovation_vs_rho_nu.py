import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 18

innovation_types = {"explorative": "Explorative", "exploitative": "Exploitative"}

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

# Define the custom palette using the desired colors
custom_palette = [
    my_color["red"],
    my_color["light_blue"],
    my_color["light_green"],
    my_color["purple"],
    my_color["yellow"],
]

for innovation_type, name in innovation_types.items():

    # Load the CSV data into DataFrames
    full_search_df = pd.read_csv(f"../../full_search/results/{innovation_type}/output.csv")

    # Add a new column 'rho_over_nu' which is the result of rho / full_search_df
    full_search_df['rho_over_nu'] = full_search_df['rho'] / full_search_df['nu']

    # Plot NCTF vs. rho/nu for each distinct rho value with custom colors
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=full_search_df, x='rho_over_nu', y='nctf_mean', hue='rho', markers=True, palette=custom_palette)
    plt.xlabel('$\\rho / \\nu$', fontsize=24)
    plt.ylabel('NCTF', fontsize=24)
    plt.title(f"NCTF vs. $\\rho / \\nu$: {innovation_types[innovation_type]} Innovation")
    plt.legend(title='$\\rho$')
    plt.tight_layout()
    plt.savefig(f"../results/NCTF_vs_rho_over_nu_{innovation_type}.png", dpi=300)  # Save the plot as an image
    plt.close()

    # Plot TTF vs. rho/nu for each distinct rho value with custom colors
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=full_search_df, x='rho_over_nu', y='ttf_mean', hue='rho', markers=True, palette=custom_palette)
    plt.xlabel('$\\rho / \\nu$', fontsize=24)
    plt.ylabel('TTF', fontsize=24)
    plt.title(f"TTF vs. $\\rho / \\nu$: {innovation_types[innovation_type]} Innovation")
    plt.legend(title='$\\rho$')
    plt.tight_layout()
    plt.savefig(f"../results/TTF_vs_rho_over_nu_{innovation_type}.png", dpi=300)  # Save the plot as an image
    plt.close()
