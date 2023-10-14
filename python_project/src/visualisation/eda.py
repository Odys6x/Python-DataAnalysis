import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import pandas as pd


class EDA:
    def __init__(self, df, name):
        """This __init__ method takes in a Pandas DataFrame and hotel name to facilitate sentiment analysis."""
        self.df = df
        self.name = name

    @classmethod
    def create_instance(cls, data, selected_name):
        # Filter the DataFrame based on the selected name
        filtered_df = data[data["name"] == selected_name]
        eda = cls(filtered_df, selected_name)
        return eda

    def plot_review_count_by_rating(self):
        st.title("Review Count by Rating")
        rating_counts = self.df["rating"].value_counts().sort_index()
        st.bar_chart(rating_counts)
