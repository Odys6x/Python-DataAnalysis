# import sys
# import pandas as pd

# sys.path.insert(0, "src/data_cleaning")

# from cleaning import DataCleaning


# filepath = "data/raw/refined.csv"
# df = pd.read_csv(filepath)

# data_cleaner = DataCleaning()
# cleaned_new_df = data_cleaner.cleaned_df(df)

# print(cleaned_new_df)
import os

# get the current working directory
current_working_directory = os.getcwd()

# print output to the console
print(current_working_directory)
