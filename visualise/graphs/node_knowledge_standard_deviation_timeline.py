import pandas as pd
import matplotlib.pyplot as plt

types = {"nctf": "NCTF", "ttf": "TTF"}

for type, name in types.items():
    # Load the CSV data into DataFrames
    best_df = pd.read_csv(f"../../full_search/results/explorative/best_worst/best_{type}.csv")
    worst_df = pd.read_csv(f"../../full_search/results/explorative/best_worst/worst_{type}.csv")

    best_rho = best_df["rho"].iloc[0]
    worst_rho = worst_df["rho"].iloc[0]

    best_nu = best_df["nu"].iloc[0]
    worst_nu = worst_df["nu"].iloc[0]

    # Helper function to process 'standard_deviation_history' column and ensure median length
    def process_df(df):
        df["standard_deviation_history"] = df["standard_deviation_history"].apply(lambda x: list(map(float, x.split('|'))))
        median_steps = int(df["standard_deviation_history"].apply(len).median())
        
        for index, row in df.iterrows():
            if len(row["standard_deviation_history"]) > median_steps:
                df.at[index, "standard_deviation_history"] = row["standard_deviation_history"][:median_steps]
            elif len(row["standard_deviation_history"]) < median_steps:
                difference = median_steps - len(row["standard_deviation_history"])
                df.at[index, "standard_deviation_history"] += [None]*difference
        return df, median_steps

    # Process both DataFrames
    best_df, median_steps_min = process_df(best_df)
    worst_df, median_steps_max = process_df(worst_df)

    # Compute average standard deviations for min and max df
    def compute_avg_std(df, median_steps):
        average_std_deviations = []
        for step in range(median_steps):
            step_values = [row[step] for row in df["standard_deviation_history"] if row[step] is not None]
            average_std = sum(step_values) / len(step_values)
            average_std_deviations.append(average_std)
        return average_std_deviations

    avg_std_dev_min = compute_avg_std(best_df, median_steps_min)
    avg_std_dev_max = compute_avg_std(worst_df, median_steps_max)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(avg_std_dev_min, label=f"Min {name} (rho={best_rho}, nu={best_nu})", color='green')
    plt.plot(avg_std_dev_max, label=f"Max {name} (rho={worst_rho}, nu={worst_nu})", color='red')
    plt.xlabel("Time Step")
    plt.ylabel("Average Standard Deviation of Node Knowledge")
    plt.title(f"Evolution of Standard Deviation of Node Knowledge: {name}")
    plt.legend()

    # Save the figure to a file
    plt.savefig(f"../results/average_std_deviation_evolution_{type}.png")
