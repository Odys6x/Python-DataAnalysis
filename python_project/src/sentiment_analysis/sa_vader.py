'''
sa_vader.py - Module containing functions for performing sentiment analysis on given dataset.
Created by Ashsyahid H, October 2023.
Released intto the public domain.
'''
import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import math
import csv
from scipy.special import softmax
from transformers import pipeline
from transformers import AutoTokenizer
import urllib.request
from transformers import AutoModelForSequenceClassification

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)


class SentimentAnalyzer:

    def __init__(self, df, name):
        '''This __init__ method takes in a Pandas DataFrame and hotel name to facilitate sentiment analysis.'''
        self.df = df
        self.name = name
        self.attribute = {"admiration": 2, "amusement": 2, "approval": 2, "caring": 2, "desire": 2, "excitement": 2,
                          "gratitude": 2, "joy": 2, "love": 2, "optimism": 2, "pride": 2,
                          "confusion": 1, "curiosity": 1, "realization": 1, "surprise": 1, "neutral": 1,
                          "anger": 0, "annoyance": 0, "dissapointment": 0, "disapproval": 0, "disgust": 0,
                          "embarrassment": 0, "fear": 0, "grief": 0, "nervousness": 0, "remorse": 0, "sadness": 0}

    def categorize(self, score):
        '''This method takes in an argument 'score' and returns the sentiment based on the categorized value.'''
        if score > 0.25:
            # pos
            return 'positive'
        elif score < -0.25:
            # neg
            return 'negative'
        else:
            # neutral
            return 'neutral'

    def preprocess(self,text):
        new_text = [
        ]
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def preprocess_text(self, text):
        '''This method performs preprocessing on the input text.'''
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
        processed_text = ' '.join(lemmatized_tokens)

        return processed_text

    def analyze_sentiment(self):
        '''This method performs sentiment analysis on the given Pandas DataFrame.'''
        self.df.columns = [x.lower() for x in self.df.columns]
        df = self.df.filter(['name', 'average_rating', 'rating', 'comment_content', 'date'], axis=1)
        df.dropna(inplace=True)
        # hotel_name variable depends on user input i.e choose what hotel to perform SA on
        df = df[df.loc[:, ['name']].values == self.name]
        # preprocess data
        df['comment_content'] = df['comment_content'].apply(self.preprocess_text)
        analyzer = SentimentIntensityAnalyzer()
        df['scores'] = df['comment_content'].apply(lambda review: analyzer.polarity_scores(review))
        df['compound_score'] = df['scores'].apply(lambda d: d['compound'])
        df['sentiment'] = df['compound_score'].apply(self.categorize)
        return df

    def analyze_emotions(self):
        '''This method performs sentiment analysis on emotions in given Pandas DataFrame.'''
        d = {"name": [], "emotions": [], "points": [], "ratings": []}
        self.df.columns = [x.lower() for x in self.df.columns]
        df = self.df
        df = df[df.loc[:, ['name']].values == self.name]
        attr = self.attribute
        for index, row in df.iloc[:].iterrows():
            cumulative_scores = {}
            t = row['comment_content']
            if len(t) > 501:
                split_text = [t[i:i + 500] for i in range(0, len(t), 500)]
                for i, segment in enumerate(split_text, 1):
                    results = classifier([segment])
                    for results in results:
                        for entry in results:
                            label = entry['label']
                            score = entry['score']
                            if label not in cumulative_scores:
                                cumulative_scores[label] = 0
                            cumulative_scores[label] += score
                label_scores = list(cumulative_scores.items())
                # Sort the list based on the score in descending order
                sorted_labels = sorted(label_scores, key=lambda x: x[1], reverse=True)
                sorted_labels_as_dicts = [{'label': label, 'score': score} for label, score in sorted_labels]
            else:
                results = classifier([t])
                sorted_labels_as_dicts = sorted(results[0], key=lambda x: x['score'], reverse=True)
            emotions = [entry['label'] for entry in sorted_labels_as_dicts[0:5]]
            points = 0
            for i in emotions:
                if i in attr:
                    points += float(attr[i])
            points = math.ceil(points / 2)
            if points == 0:
                points = 1
            d['name'].append(row["name"])
            d['emotions'].append(emotions)
            d['points'].append(float(points))
            d["ratings"].append(row['rating'])

            df = pd.DataFrame.from_dict(d)
        return df

    def analyze_sarcasm(self):
        task = 'irony'
        MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
        sarcasm = {'IsSarcasm': []}
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        labels = []
        mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
        with urllib.request.urlopen(mapping_link) as f:
            html = f.read().decode('utf-8').split("\n")
            csvreader = csv.reader(html, delimiter='\t')
        labels = [row[1] for row in csvreader if len(row) > 1]
        # PT
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)

        df = self.df
        df = df[df.loc[:, ['name']].values == self.name]
        sarcasm = {'IsSarcasm': []}

        # Assuming you've initialized tokenizer and model
        for i, row in df.iterrows():
            text = row['comment_content']
            if len(text) > 500:
                split_text = [text[i:i + 500] for i in range(0, len(text), 500)]
            else:
                split_text = [text]
            total_sScore = 0
            total_slScore = 0
            for segment in split_text:
                # Preprocess the segment

                segment = self.preprocess(segment)

                # Model inference
                encoded_input = tokenizer(segment, return_tensors='pt')
                output = model(**encoded_input)
                scores = output[0][0].detach().numpy()
                scores = softmax(scores)
                ranking = np.argsort(scores)

                l = labels[ranking[0]]
                s = scores[ranking[0]]
                ls = labels[ranking[1]]
                sl = scores[ranking[1]]
                total_sScore += s
                total_slScore += sl

            if total_slScore > total_sScore:
                sarcasm['IsSarcasm'].append(ls)
            else:
                sarcasm['IsSarcasm'].append(l)


        sarcasmdf = pd.DataFrame.from_dict(sarcasm)

        return sarcasmdf