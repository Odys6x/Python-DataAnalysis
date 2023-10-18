import pandas as pd
import os

"""
    Merges all the individual hotel review CSV files from the input directory into a single DataFrame,
    removes duplicates based on the 'Comment_content' column, and saves the merged
    DataFrame to csv.

    Parameters:
    input_directory (str): The path to the directory containing CSV files to be merged.
    output_file (str): The path to save the merged CSV file.

"""


def merge_csv_files(input_directory, output_file):
    dataframes = []

    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_directory, filename)
            df = pd.read_csv(filepath)
            dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_df = merged_df.drop_duplicates(subset=["Comment_content"])

    merged_df.to_csv(output_file, index=False)
    print(f"Merged data saved to {output_file}")


if __name__ == "__main__":
    input_directory = "../data/raw/individual_hotel"
    output_file = "../data/raw/Finalised_Total_Reviews.csv"
    merge_csv_files(input_directory, output_file)
