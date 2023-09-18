import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 18

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

# Load the CSV data into DataFrames
explorative_df = pd.read_csv("../../full_search/results/explorative/output.csv")

# Add a new column 'rho_over_nu' which is the result of rho / nu
explorative_df['rho_over_nu'] = explorative_df['rho'] / explorative_df['nu']

# Define the custom title text
custom_title = ""

# Plot NCTF vs. rho/nu for each distinct rho value with custom colors
plt.figure(figsize=(10, 6))
sns.lineplot(data=explorative_df, x='rho_over_nu', y='nctf_mean', hue='rho', markers=True, palette=my_color)
plt.xlabel(r'$\frac{\rho}{\nu}$', fontsize=24)  # Use LaTeX symbols
plt.ylabel('NCTF', fontsize=24)
plt.title(custom_title + 'NCTF vs. ' + r'$\frac{\rho}{\nu}$')
plt.legend(title='$\\rho$')
plt.tight_layout()
plt.savefig('../results/NCTF_vs_rho_over_nu.png', dpi=300)  # Save the plot as an image
plt.close()

# Plot TTF vs. rho/nu for each distinct rho value with custom colors
plt.figure(figsize=(10, 6))
sns.lineplot(data=explorative_df, x='rho_over_nu', y='ttf_mean', hue='rho', markers=True, palette=my_color)
plt.xlabel(r'$\frac{\rho}{\nu}$', fontsize=24)  # Use LaTeX symbols
plt.ylabel('TTF', fontsize=24)
plt.title(custom_title + 'TTF vs. ' + r'$\frac{\rho}{\nu}$')
plt.legend(title='$\\rho$')
plt.tight_layout()
plt.savefig('../results/TTF_vs_rho_over_nu.png', dpi=300)  # Save the plot as an image
plt.close()