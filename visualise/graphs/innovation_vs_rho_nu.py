import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV data into DataFrames
explorative_df = pd.read_csv("../../full_search/results/explorative/output.csv")

# Add a new column 'rho_over_nu' which is the result of rho / nu
explorative_df['rho_over_nu'] = explorative_df['rho'] / explorative_df['nu']

# Define the custom title text
custom_title = "Explorative Innovation: "

# Plot NCTF vs. rho/nu
plt.figure(figsize=(10, 5))
plt.scatter(explorative_df['rho_over_nu'], explorative_df['nctf_mean'], label='NCTF')
plt.xlabel(r'$\frac{\rho}{\nu}$')  # Use LaTeX symbols
plt.ylabel('NCTF Mean')
plt.title(custom_title + '\nNCTF vs. ' + r'$\frac{\rho}{\nu}$')
plt.legend()
plt.savefig('../results/NCTF_vs_rho_over_nu.png')  # Save the plot as an image
plt.close()

# Plot TTF vs. rho/nu
plt.figure(figsize=(10, 5))
plt.scatter(explorative_df['rho_over_nu'], explorative_df['ttf_mean'], label='TTF', color='orange')
plt.xlabel(r'$\frac{\rho}{\nu}$')  # Use LaTeX symbols
plt.ylabel('TTF Mean')
plt.title(custom_title + '\nTTF vs. ' + r'$\frac{\rho}{\nu}$')
plt.legend()
plt.savefig('../results/TTF_vs_rho_over_nu.png')  # Save the plot as an image
plt.close()
