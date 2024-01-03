import pandas as pd
import os

if __name__ == "__main__":
    import os
    import pandas as pd

    target = "eight"
    input_directory = f"../data/networks/{target}/raw"
    output_directory = f"../data/networks/{target}/processed"

    # Initialize an empty list to store DataFrames
    dfs = []

    # Loop through files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            # Construct the full file path
            file_path = os.path.join(input_directory, filename)
            
            # Read the CSV file and append it to the list of DataFrames
            df = pd.read_csv(file_path)
            dfs.append(df)

    # Concatenate all DataFrames into one
    concatenated_df = pd.concat(dfs, ignore_index=True)

    # Select the desired columns
    columns_to_keep = ['ego_person_hash', 'alter_person_hash']
    selected_df = concatenated_df[columns_to_keep]
    
    new_column_names = {'ego_person_hash': 'caller', 'alter_person_hash': 'callee'}
    selected_df = selected_df.rename(columns=new_column_names)

    # Write the selected DataFrame to a CSV file
    selected_df.to_csv(f'{output_directory}/eight_processed.csv', index=False)