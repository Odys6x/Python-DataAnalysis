import pandas as pd
import os

# Specify the directory containing the CSV files
directory = "../data/raw/individual_hotel"

# Initialize an empty list to store DataFrames
dataframes = []

# Iterate over all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        dataframes.append(df)

# Concatenate all DataFrames into one
merged_df = pd.concat(dataframes, ignore_index=True)

# Remove duplicates based on a subset of columns (adjust as needed)
# For example, if you want to remove duplicates based on "Name" and "Date":
merged_df = merged_df.drop_duplicates(subset=["Comment_content"])

# Save the final merged DataFrame to a new CSV file
merged_csv_filename = "../data/raw/Finalised_Total_Reviews.csv"
merged_df.to_csv(merged_csv_filename, index=False)

print(f"Merged data saved to {merged_csv_filename}")
