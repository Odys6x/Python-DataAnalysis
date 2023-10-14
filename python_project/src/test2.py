import pandas as pd
from data_cleaning.cleaning import DataCleaning
from visualisation.eda import EDA

df1 = pd.read_csv("data/raw/Finalised_Total_Reviews.csv")
df2 = pd.read_csv("data/raw/Hotel_List.csv")
data = pd.merge(df1, df2, on="Name", how="left")
data_cleaner = DataCleaning()
cleaned_new_df = data_cleaner.cleaned_df(data)

eda = EDA(data)

# Call the plot_rating_counts method to create the plot
eda.plot_review_count_by_rating()
