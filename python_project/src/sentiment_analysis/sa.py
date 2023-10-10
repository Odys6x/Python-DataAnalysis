from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys


sys.path.insert(0, "src/data_cleaning")

from cleaning import DataCleaning


data_cleaner = DataCleaning()
df = data_cleaner.cleaned_df()


class Sentiment_analysis:
    """
    A class for performing sentiment analysis on a DataFrame using VADER sentiment analysis.

    Methods
    -------
    vader_polarity()
        Calculate VADER sentiment polarity scores for comments.

    compound_score_by_rating(vaders)
        Create a barplot of compound sentiment scores by rating.

    polarity_score_by_rating(vaders)
        Create barplots of positive, neutral, and negative sentiment scores by rating.
    """

    def vader_polarity(self):
        """
        Calculate VADER sentiment polarity scores for comments.

        Returns
        -------
        pandas.DataFrame
            DataFrame with VADER sentiment scores.
        """
        sia = SentimentIntensityAnalyzer()
        res = {}
        for i, row in df.iterrows():
            text = row["comment_content"]
            myid = row["index"]
            res[myid] = sia.polarity_scores(text)
        vaders = pd.DataFrame(res).T
        vaders = vaders.reset_index().rename(columns={"index": "index"})
        vaders = vaders.merge(df, how="left")

        return vaders

    def compound_score_by_rating(self, vaders):
        """
        Create a barplot of compound sentiment scores by rating.

        Parameters
        ----------
        vaders : pandas.DataFrame
            DataFrame with VADER sentiment scores.

        Returns
        -------
        None
        """
        ax = sns.barplot(data=vaders, x="rating", y="compound", errorbar=None)
        ax.set_title("Compound Score by Rating")
        plt.show()

    def polarity_score_by_rating(self, vaders):
        """
        Create barplots of positive, neutral, and negative sentiment scores by rating.

        Parameters
        ----------
        vaders : pandas.DataFrame
            DataFrame with VADER sentiment scores.

        Returns
        -------
        None
        """
        fig, axs = plt.subplots(1, 3, figsize=(12, 3))
        sns.barplot(data=vaders, x="rating", y="pos", ax=axs[0], errorbar=None)
        sns.barplot(data=vaders, x="rating", y="neu", ax=axs[1], errorbar=None)
        sns.barplot(data=vaders, x="rating", y="neg", ax=axs[2], errorbar=None)
        axs[0].set_title("Positive")
        axs[1].set_title("Neutral")
        axs[2].set_title("Negative")
        plt.tight_layout()
        plt.show()
