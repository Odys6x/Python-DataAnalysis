import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, "src/data_cleaning")

from cleaning import DataCleaning


data_cleaner = DataCleaning()
df = data_cleaner.cleaned_df()


class Eda:
    def count_by_rating(self):
        ax = (
            df["rating"]
            .value_counts()
            .sort_index()
            .plot(kind="bar", title="Count of Reviews by rating", figsize=(10, 5))
        )
        ax.set_xlabel("Rating")
        plt.show()
