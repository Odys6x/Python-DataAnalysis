import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import pandas as pd


class EDA:
    def __init__(self, df, name=None):
        """This __init__ method takes in a Pandas DataFrame and an optional hotel name to facilitate sentiment analysis."""
        self.df = df
        self.name = name

    @classmethod
    def create_instance(cls, data, selected_name):
        # Filter the DataFrame based on the selected name
        filtered_df = data[data["name"] == selected_name]
        eda = cls(filtered_df, selected_name)
        return eda

    def plot_review_count_by_rating(self):
        rating_counts = self.df["rating"].value_counts().sort_index()

        # Create a bar chart with Plotly Express
        fig = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={"x": "Rating", "y": "Review Count"},
        )

        # Customize the x-axis orientation
        fig.update_xaxes(tickangle=0)  # Rotate x-axis labels by 45 degrees

        st.plotly_chart(fig, use_container_width=True)

    def plot_average_price_by_rating(self):
        average_price_by_rating = self.df.groupby("rating")["price"].mean()
        fig = px.bar(x=average_price_by_rating.index, y=average_price_by_rating.values)
        fig.update_layout(
            xaxis_title="Rating",
            yaxis_title="Average Price",
            title="Average Price by Rating for all hotels",
        )
        st.plotly_chart(fig)

    def plot_grouped_bar_chart_for_avg_categories(self):
        # Select columns 'location', 'cleanliness', 'service', and 'value'
        selected_columns = ["location", "cleanliness", "service", "value"]

        # Calculate the average of selected columns for each rating
        avg_ratings = self.df.groupby("rating")[selected_columns].mean()

        # Melt the dataframe to create a long format for Plotly Express
        melted_df = avg_ratings.reset_index().melt(
            id_vars="rating", var_name="category", value_name="avg_score"
        )

        # Create a grouped bar chart with Plotly Express
        fig = px.bar(
            melted_df,
            x="rating",
            y="avg_score",
            color="category",
            title="Average Ratings for Selected Categories for all hotels",
            barmode="group",  # Grouped bars
        )

        st.plotly_chart(fig)

    def plot_average_hotel_class_by_rating(self):
        average_price_by_rating = self.df.groupby("hotel_class")["rating"].mean()
        fig = px.bar(x=average_price_by_rating.index, y=average_price_by_rating.values)
        fig.update_layout(
            xaxis_title="Hotel Class",
            yaxis_title="Average Rating",
            title="Average Rating by Hotel Class for all hotels",
        )
        st.plotly_chart(fig)
