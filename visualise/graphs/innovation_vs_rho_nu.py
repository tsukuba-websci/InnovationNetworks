import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 18


# Load the CSV data into DataFrames
explorative_df = pd.read_csv("../../full_search/results/explorative/output.csv")

# Add a new column 'rho_over_nu' which is the result of rho / nu
explorative_df['rho_over_nu'] = explorative_df['rho'] / explorative_df['nu']

# Define the custom title text
custom_title = "Explorative Innovation: "

# Plot NCTF vs. rho/nu for each distinct rho value
plt.figure(figsize=(10, 6))
sns.lineplot(data=explorative_df, x='rho_over_nu', y='nctf_mean', hue='rho', markers=True, palette='tab10')
plt.xlabel(r'$\frac{\rho}{\nu}$', fontsize=24)  # Use LaTeX symbols
plt.ylabel('NCTF Mean', fontsize=24)
plt.title(custom_title + 'NCTF vs. ' + r'$\frac{\rho}{\nu}$')
plt.legend(title='$\\rho$')
plt.tight_layout()
plt.savefig('../results/NCTF_vs_rho_over_nu.png', dpi=300)  # Save the plot as an image
plt.close()

# Plot TTF vs. rho/nu for each distinct rho value
plt.figure(figsize=(10, 6))
sns.lineplot(data=explorative_df, x='rho_over_nu', y='ttf_mean', hue='rho', markers=True, palette='tab10')
plt.xlabel(r'$\frac{\rho}{\nu}$', fontsize=24)  # Use LaTeX symbols
plt.ylabel('TTF Mean', fontsize=24)
plt.title(custom_title + 'TTF vs. ' + r'$\frac{\rho}{\nu}$')
plt.legend(title='$\\rho$')
plt.tight_layout()
plt.savefig('../results/TTF_vs_rho_over_nu.png', dpi=300)  # Save the plot as an image
plt.close()
