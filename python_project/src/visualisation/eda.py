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
        
def plot_amenities_by_rating(self):
    st.title("Amenities vs Rating")
    
    # Split the 'amenities' column by comma and space, and flatten the resulting list of amenities
    amenities_split = self.df['amenities'].str.split(', ').explode()
    rating=self.df['hotel_average_ratings']
    # Count the frequency of each amenity
    amenity_counts = amenities_split.value_counts()

    # Create a scatter plot using Plotly Express
    fig = px.scatter(self.df, x=rating, y=amenity_counts.values, title='Amenity Count vs Rating')
    fig.update_xaxes(title='Amenity')
    fig.update_yaxes(title='Rating')
    
    st.plotly_chart(fig)