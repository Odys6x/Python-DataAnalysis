import ast
import sys
from collections import Counter
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from wordcloud import WordCloud


class Visualise:
    def __init__(self, df, name):
        """This __init__ method takes in a Pandas DataFrame and hotel name to facilitate sentiment analysis."""
        self.df = df
        self.name = name

    def visualise_ratings(self):
        """
        This function plots the relationship between original ratings and machine learning produced rating for the selected hotel.

        Returns:
            None
        """
        st.subheader("Bar Chart Comparison")
        df = self.df
        original_ratings = df["ratings"]
        produced_ratings = df["points"]
        # Create a histogram-like effect for bar chart
        original_counts, original_bins = np.histogram(
            original_ratings, bins=range(1, 7)
        )
        produced_counts, produced_bins = np.histogram(
            produced_ratings, bins=range(1, 7)
        )

        # Create a bar chart for original ratings
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=original_bins[:-1],
                y=original_counts,
                name="Original Ratings",
                marker_color="#44528d",
            )
        )

        # Create a bar chart for produced ratings
        fig.add_trace(
            go.Bar(
                x=produced_bins[:-1],
                y=produced_counts,
                name="Produced Ratings",
                marker_color="#D8BFD8",
            )
        )

        # Update layout
        fig.update_layout(
            title="Frequency vs. Ratings",
            xaxis_title="Ratings",
            yaxis_title="Frequency",
            barmode="group",
            showlegend=True,
        )

        # Show the plot
        st.plotly_chart(fig, use_container_width=True)

    def visualise_emotions(self):
        """
        This function plots the 28 emotions of how the customer feels towwards the hotel.

        Returns:
            None
        """
        df = self.df
        st.subheader("How customers are feeling?")
        target_words = [
            "admiration",
            "amusement",
            "approval",
            "caring",
            "desire",
            "excitement",
            "gratitude",
            "joy",
            "love",
            "optimism",
            "pride",
            "confusion",
            "curiosity",
            "realization",
            "surprise",
            "neutral",
            "anger",
            "annoyance",
            "disappointment",
            "disapproval",
            "disgust",
            "embarrassment",
            "fear",
            "grief",
            "nervousness",
            "remorse",
            "sadness",
        ]

        word_counts = {word: 0 for word in target_words}
        title = self.name

        # Loop through each data row
        for i, row in df.iterrows():
            # Split the row into words
            words = row["emotions"]

            # Count occurrences of target words
            words = ast.literal_eval(str(words))
            for word in words:
                if word in target_words:
                    word_counts[word] += 1

        # Create a new dictionary with three-letter codes as keys
        top_5_items = sorted(
            word_counts.items(), key=lambda item: item[1], reverse=True
        )[:5]

        # Convert the list of tuples back to a dictionary
        top_5_dict = dict(top_5_items)

        # Extract keys and values
        x_values = list(word_counts.keys())
        y_values = list(word_counts.values())
        x_value = list(top_5_dict.keys())
        y_value = list(top_5_dict.values())

        # Create a bar chart
        figu = go.Figure()
        pastel_color = ["#FFB6C1"]
        figu.add_trace(go.Bar(x=x_values, y=y_values, marker_color="#FFB6C1"))

        # Add labels and title
        figu.update_layout(title=title, xaxis_title="Emotions", yaxis_title="Counts")

        st.plotly_chart(figu, use_container_width=True)

        # Create a bar chart
        figur = go.Figure()

        figur.add_trace(go.Bar(x=x_value, y=y_value, marker_color="#FFC0CB"))

        # Add labels and title
        figur.update_layout(title=title, xaxis_title="Emotions", yaxis_title="Counts")

        st.plotly_chart(figur, use_container_width=True)

    def visualise_wordcloud(self):
        """This function creates a word cloud for positive and negative sentiments"""
        name = self.name
        df = self.df
        # filter df to retrieve positive and negative sentiments
        df_pos = df.loc[df["sentiment"] == "positive"]
        df_neg = df.loc[df["sentiment"] == "negative"]

        text_pos = "".join(comment for comment in df_pos["comment_content"])
        word_cloud_pos = WordCloud(
            collocations=False, background_color="black", width=800, height=400
        ).generate(text_pos)
        text_neg = "".join(comment for comment in df_neg["comment_content"])
        word_cloud_neg = WordCloud(
            collocations=False, background_color="black", width=800, height=400
        ).generate(text_neg)
        # plot positive word cloud
        st.subheader(f"Positive word Cloud for {name}")
        plt.imshow(word_cloud_pos, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
        # plot negative word cloud
        st.subheader(f"Negative word Cloud for {name}")
        plt.imshow(word_cloud_neg, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)

    def visualise_sentiment(self):
        df = self.df
        chart1, chart2 = st.columns(2)

        # Sentiment Histogram
        with chart1:
            st.subheader("Histogram")
            sentiment_counts = df["sentiment"]
            fig = px.histogram(df, x="sentiment", color="sentiment")
            fig.update_xaxes(categoryorder="array", categoryarray=["neg", "neu", "pos"])
            histogram = go.Figure(fig)
            st.plotly_chart(histogram, use_container_width=True)
        # Sentiment Donut Chart
        with chart2:
            st.subheader("Donut chart")
            sentiment_counts = df["sentiment"]
            fig = px.pie(df, names="sentiment", hole=0.3)
            pie = go.Figure(fig)
            st.plotly_chart(pie, use_container_width=True)

    def visualise_sarcasm(self):
        """
        This function plots a donut chart of the number of sarcastic words non sarcastic words.

        Returns:
            None
        """
        df = self.df
        st.subheader("Donut chart")
        fig = px.pie(df, names="IsSarcasm", hole=0.3)
        pie = go.Figure(fig)
        st.plotly_chart(pie, use_container_width=True)
