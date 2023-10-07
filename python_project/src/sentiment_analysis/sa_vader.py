'''
sa_vader.py - Module containing functions for performing sentiment analysis on given dataset.
Created by Ashsyahid H, October 2023. 
Released intto the public domain.
'''
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyzer:

    def __init__(self, df, name):
        '''This __init__ method takes in a Pandas DataFrame and hotel name to facilitate sentiment analysis.'''
        self.df = df
        self.name = name

    def categorize(self, score):
        '''This method takes in an argument 'score' and returns the sentiment based on the categorized value.'''
        if score > 0.25:
            # pos
            return 'pos'
        elif score < -0.25:
            # neg
            return 'neg'
        else:
            # neutral
            return 'neu'

    def analyze_sentiment(self):
        '''This method performs sentiment analysis on the given Pandas DataFrame.'''
        self.df.columns = [x.lower() for x in self.df.columns]
        df = self.df.filter(['name', 'average_rating', 'rating', 'comment_content', 'date'], axis = 1)
        df.dropna(inplace = True)
        # hotel_name variable depends on user input i.e choose what hotel to perform SA on
        df = df[df.loc[:, ['name']].values == self.name]
        analyzer = SentimentIntensityAnalyzer()
        df['scores'] = df['comment_content'].apply(lambda review: analyzer.polarity_scores(review))
        df['compound_score'] = df['scores'].apply(lambda d:d['compound'])
        df['sentiment'] = df['compound_score'].apply(self.categorize)
        return df
