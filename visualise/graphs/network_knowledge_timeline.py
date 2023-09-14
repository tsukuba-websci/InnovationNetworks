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

    # Helper function to process 'total_knowledge_history' column and ensure median length
    def process_df(df):
        df["total_knowledge_history"] = df["total_knowledge_history"].apply(lambda x: list(map(float, x.split('|'))))
        median_steps = int(df["total_knowledge_history"].apply(len).median())
        
        for index, row in df.iterrows():
            if len(row["total_knowledge_history"]) > median_steps:
                df.at[index, "total_knowledge_history"] = row["total_knowledge_history"][:median_steps]
            elif len(row["total_knowledge_history"]) < median_steps:
                difference = median_steps - len(row["total_knowledge_history"])
                df.at[index, "total_knowledge_history"] += [None]*difference
        return df, median_steps

    # Process both DataFrames
    best_df, median_steps_min = process_df(best_df)
    worst_df, median_steps_max = process_df(worst_df)

    # Compute average total knowledge for min and max df
    def compute_avg_knowledge(df, median_steps):
        average_knowledge = []
        for step in range(median_steps):
            step_values = [row[step] for row in df["total_knowledge_history"] if row[step] is not None]
            avg_know = sum(step_values) / len(step_values)
            average_knowledge.append(avg_know)
        return average_knowledge

    avg_knowledge_min = compute_avg_knowledge(best_df, median_steps_min)
    avg_knowledge_max = compute_avg_knowledge(worst_df, median_steps_max)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(avg_knowledge_min, label=f"Min {name} (rho={best_rho}, nu={best_nu})", color='green')
    plt.plot(avg_knowledge_max, label=f"Max {name} (rho={worst_rho}, nu={worst_nu})", color='red')
    plt.xlabel("Time Step")
    plt.ylabel("Average Total Knowledge")
    plt.title(f"Evolution of Average Total Knowledge Over Time: {name}")
    plt.legend()

    # Save the figure to a file
    plt.savefig(f"../results/average_knowledge_evolution_{type}.png")
