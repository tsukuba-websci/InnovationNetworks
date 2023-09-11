import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into DataFrames
min_df = pd.read_csv(f"../../qd/results/min_NCTF/best_nctf_scores.csv")
max_df = pd.read_csv(f"../../qd/results/max_NCTF/best_nctf_scores.csv")

min_rho = min_df["rho"].iloc[0]
max_rho = max_df["rho"].iloc[0]

min_nu = min_df["nu"].iloc[0]
max_nu = max_df["nu"].iloc[0]

# Helper function to process 'Standard Deviation History' column and ensure median length
def process_df(df):
    df["Standard Deviation History"] = df["Standard Deviation History"].apply(lambda x: list(map(float, x.split('|'))))
    median_steps = int(df["Standard Deviation History"].apply(len).median())
    
    for index, row in df.iterrows():
        if len(row["Standard Deviation History"]) > median_steps:
            df.at[index, "Standard Deviation History"] = row["Standard Deviation History"][:median_steps]
        elif len(row["Standard Deviation History"]) < median_steps:
            difference = median_steps - len(row["Standard Deviation History"])
            df.at[index, "Standard Deviation History"] += [None]*difference
    return df, median_steps

# Process both DataFrames
min_df, median_steps_min = process_df(min_df)
max_df, median_steps_max = process_df(max_df)

# Compute average standard deviations for min and max df
def compute_avg_std(df, median_steps):
    average_std_deviations = []
    for step in range(median_steps):
        step_values = [row[step] for row in df["Standard Deviation History"] if row[step] is not None]
        average_std = sum(step_values) / len(step_values)
        average_std_deviations.append(average_std)
    return average_std_deviations

avg_std_dev_min = compute_avg_std(min_df, median_steps_min)
avg_std_dev_max = compute_avg_std(max_df, median_steps_max)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(avg_std_dev_min, label=f"Min NCTF (rho={min_rho}, nu={min_nu})", color='blue')
plt.plot(avg_std_dev_max, label=f"Max NCTF (rho={max_rho}, nu={max_nu})", color='red')
plt.xlabel("Time Step")
plt.ylabel("Average Standard Deviation of Node Knowledge")
plt.title("Evolution of Standard Deviation of Node Knowledge")
plt.legend()

# Save the figure to a file
plt.savefig("../results/average_std_deviation_evolution.png")
