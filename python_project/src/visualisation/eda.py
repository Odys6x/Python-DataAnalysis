import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.express as px
import altair as alt


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
    @classmethod
    def create_instance_all(cls,data):
        eda=cls(data,name=None)
        return eda

    def plot_review_count_by_rating(self):
        st.title("Review Count by Rating")
        rating_counts = self.df["rating"].value_counts().sort_index()
        st.bar_chart(rating_counts)
    
    
    def plot_amenities_by_rating(self):
        st.title("Unique Hotels: Amenities Count and Rating")

        # Split the "Amenities" column and count the amenities for each row
        self.df['amenities_list'] = self.df['amenities'].str.split(', ')
        self.df['amenities_count'] = self.df['amenities_list'].apply(len)

        # Group by unique hotel names, calculate the mean rating and sum of amenities count
        grouped_df = self.df.groupby('name', as_index=False).agg({
            'amenities_count': 'first',
            'hotel_average_ratings': 'first'
        })

        # Create a scatter plot using Plotly Express with color based on mean rating
        fig = px.scatter(
            grouped_df,
            x='name',
            y='amenities_count',
            color='hotel_average_ratings',
            title="Unique Hotels: Amenities Count vs. Rating",
            labels={'name': 'Hotel Name', 'amenities_count': 'Amenities Count', 'hotel_average_ratings': 'Rating'},
            color_continuous_scale='Viridis',  # Choose a color scale
        )
        fig.update_traces(marker=dict(size=12))  # Adjust marker size

        # Customize the layout
        fig.update_layout(
            xaxis_title="Hotel Name",
            yaxis_title="Amenities Count",
            coloraxis_colorbar=dict(title="Rating"),  # Define the color axis label
        )
        # Display the plot
        st.plotly_chart(fig)

    def plot_amenities_by_rating_color_map(self):
        self.df['amenities_list'] = self.df['amenities'].str.split(', ')
        self.df['amenities_count'] = self.df['amenities_list'].apply(len)
        color_scale =px.colors.sequential.Plasma
        fig =px.scatter(
            self.df,
            x='hotel_average_ratings',
            y='amenities_count',
           
            color='hotel_average_ratings',
            text=None,
            hover_name='name',
            hover_data={'name': True}, 
            color_continuous_scale=color_scale,
            title="Hotel Ratings vs. Amenities Count"
        )
        fig.update_coloraxes(colorbar_title="Ratings")

        # Show the plot
        st.plotly_chart(fig)
        
    def plot_amenities_by_rating_box_whisker(self):
        self.df['amenities_list'] = self.df['amenities'].str.split(', ')
        self.df['amenities_count'] = self.df['amenities_list'].apply(len)

    # Create a box and whisker plot
        fig, ax = plt.subplots()
        ax.boxplot([self.df['amenities_count'], self.df['hotel_average_ratings']], vert=False, labels=['Amenities Count', 'Rating'])

    # Add labels and a title
        ax.set_xlabel('Value')
        ax.set_title('Box and Whisker Plot: Amenities Count vs. Rating')

    # Show the plot using Streamlit
        st.pyplot(fig)

