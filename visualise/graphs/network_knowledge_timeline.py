import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into DataFrames
min_df = pd.read_csv(f"../../qd/results/min_NCTF/best_nctf_scores.csv")
max_df = pd.read_csv(f"../../qd/results/max_NCTF/best_nctf_scores.csv")

min_rho = min_df["rho"].iloc[0]
max_rho = max_df["rho"].iloc[0]

min_nu = min_df["nu"].iloc[0]
max_nu = max_df["nu"].iloc[0]

# Helper function to process 'Total Knowledge History' column and ensure median length
def process_df(df):
    df["Total Knowledge History"] = df["Total Knowledge History"].apply(lambda x: list(map(float, x.split('|'))))
    median_steps = int(df["Total Knowledge History"].apply(len).median())
    
    for index, row in df.iterrows():
        if len(row["Total Knowledge History"]) > median_steps:
            df.at[index, "Total Knowledge History"] = row["Total Knowledge History"][:median_steps]
        elif len(row["Total Knowledge History"]) < median_steps:
            difference = median_steps - len(row["Total Knowledge History"])
            df.at[index, "Total Knowledge History"] += [None]*difference
    return df, median_steps

# Process both DataFrames
min_df, median_steps_min = process_df(min_df)
max_df, median_steps_max = process_df(max_df)

# Compute average total knowledge for min and max df
def compute_avg_knowledge(df, median_steps):
    average_knowledge = []
    for step in range(median_steps):
        step_values = [row[step] for row in df["Total Knowledge History"] if row[step] is not None]
        avg_know = sum(step_values) / len(step_values)
        average_knowledge.append(avg_know)
    return average_knowledge

avg_knowledge_min = compute_avg_knowledge(min_df, median_steps_min)
avg_knowledge_max = compute_avg_knowledge(max_df, median_steps_max)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(avg_knowledge_min, label=f"Min NCTF (rho={min_rho}, nu={min_nu})", color='blue')
plt.plot(avg_knowledge_max, label=f"Max NCTF (rho={max_rho}, nu={max_nu})", color='red')
plt.xlabel("Time Step")
plt.ylabel("Average Total Knowledge")
plt.title("Evolution of Average Total Knowledge Over Time")
plt.legend()

# Save the figure to a file
plt.savefig("../results/average_knowledge_evolution.png")
