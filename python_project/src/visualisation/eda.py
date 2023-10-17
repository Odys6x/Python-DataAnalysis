import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import re

class EDA:
    def __init__(self, df, name=None):
        """
        This __init__ method initialises the EDA (Exploratory Data Analysis) class with a Pandas DataFrame and an optional hotel name.

        Args:
            df (pandas.DataFrame): A Pandas DataFrame containing the data to be analyzed.
            name (str, optional): The name of the hotel to be analyzed. Defaults to None.

        Returns:
            None
        """
        self.df = df
        self.name = name

    @classmethod
    def create_instance(cls, data, selected_name):
        """
        This class method creates an instance of the EDA class by filtering the DataFrame based on the selected hotel name.

        Args:
            data (pandas.DataFrame): The source DataFrame with hotel data.
            selected_name (str): The name of the hotel to be analyzed.

        Returns:
            EDA: An instance of the EDA class with the filtered data.
        """
        # Filter the DataFrame based on the selected name
        filtered_df = data[data["name"] == selected_name]
        eda = cls(filtered_df, selected_name)
        return eda

    def plot_review_count_by_rating(self):
        """
        This function plots the review count by rating for the selected hotel.

        Returns:
            None
        """
        rating_counts = self.df["rating"].value_counts().sort_index()
        fig = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={"x": "Rating", "y": "Review Count"},
        )
        fig.update_xaxes(tickangle=0)
        st.plotly_chart(fig, use_container_width=True)

    def plot_average_price_by_rating(self):
        """
        This function plots the average price by rating for the selected hotel.

        Returns:
            None
        """
        average_price_by_rating = self.df.groupby("rating")["price"].mean()
        fig = px.bar(x=average_price_by_rating.index, y=average_price_by_rating.values)
        fig.update_layout(
            xaxis_title="Rating",
            yaxis_title="Average Price",
            title="Average Price by Rating for all hotels",
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_grouped_bar_chart_for_avg_categories(self):
        """
        This function plots a grouped bar chart for the average ratings of selected categories for the selected hotel.

        Returns:
            None
        """
        selected_columns = ["location", "cleanliness", "service", "value"]

        # Calculate the average of selected columns for each rating
        avg_ratings = self.df.groupby("rating")[selected_columns].mean()

        melted_df = avg_ratings.reset_index().melt(
            id_vars="rating", var_name="category", value_name="avg_score"
        )

        fig = px.bar(
            melted_df,
            x="rating",
            y="avg_score",
            color="category",
            title="Average Ratings for Selected Categories for all hotels",
            barmode="relative",
            category_orders={"rating": ["Low", "Medium", "High"]},
            color_discrete_sequence=px.colors.qualitative.Set3,
        )

        fig.update_layout(
            xaxis_title="Rating",
            yaxis_title="Average Score",
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_average_hotel_class_by_rating(self):
        """
        This function plots the average rating by hotel class for the selected hotel.

        Returns:
            None
        """
        average_price_by_rating = self.df.groupby("hotel_class")["rating"].mean()
        fig = px.bar(x=average_price_by_rating.index, y=average_price_by_rating.values)
        fig.update_layout(
            xaxis_title="Hotel Class",
            yaxis_title="Average Rating",
            title="Average Rating by Hotel Class for all hotels",
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_amenities_by_rating(self):
        """
        This function plots the relationship between amenities count and rating for the selected hotel.

        Returns:
            None
        """
        # Split the "Amenities" column and count the amenities for each row
        self.df["amenities_list"] = self.df["amenities"].str.split(", ")
        self.df["amenities_count"] = self.df["amenities_list"].apply(len)
        # Group by unique hotel names, calculate the mean rating and sum of amenities count
        grouped_df = self.df.groupby("name", as_index=False).agg(
            {"amenities_count": "first", "hotel_average_ratings": "first"}
        )

        fig = px.scatter(
            grouped_df,
            x="name",
            y="amenities_count",
            color="hotel_average_ratings",
            title="Amenities Count by Rating for all hotels",
            labels={
                "name": "Hotel Name",
                "amenities_count": "Amenities Count",
                "hotel_average_ratings": "Rating",
            },
        )

        fig.update_traces(marker=dict(size=6))
        st.plotly_chart(fig)

    def plot_amenities_by_rating_box_whisker(self):
        """
        This function plots a box and whisker plot for amenities count by rating for the selected hotel.

        Returns:
            None
        """
        amenities_list = self.df["amenities"].str.split(", ")
        amenities_count = amenities_list.apply(len)
        ratings = self.df["hotel_average_ratings"]

        fig = px.box(
            self.df, x=ratings, y=amenities_count, title="amenities count by rating"
        )
        fig.update_layout(yaxis_title="Amenities Count", xaxis_title="Hotel Ratings")
        fig.update_xaxes(type="linear")

        st.plotly_chart(fig, use_container_width=True)

    def plot_near_attractions_restaurants(self):
        """
        This function plots the number of nearby restaurants and attractions for the selected hotel.

        Returns:
            None
        """
        # Split the "near_attraction" column into separate columns for restaurants and attractions
        self.df["restaurants"] = (
            self.df["near_attractions"].str.extract(r"(\d+) Restaurants").astype(int)
        )
        self.df["attractions"] = (
            self.df["near_attractions"].str.extract(r"(\d+) Attractions").astype(int)
        )

        fig = px.scatter(
            self.df,
            x="restaurants",
            y="attractions",
            color="rating",
            title="Rating of Number of Restaurants vs. Number of Attractions for all hotels",
            labels={
                "restaurants": "Number of Restaurants",
                "attractions": "Number of Attractions",
            },
        )

        fig.update_traces(marker=dict(size=5))

        st.plotly_chart(fig, use_container_width=True)

    def plot_average_ratings_by_date(self):
        """
        This function plots the average ratings over years for the selected hotel.

        Returns:
            None
        """
        # Extract the month and year from the "Date of stay" column
        # self.df["date"] = pd.to_datetime(
        #     self.df["date"], format="Date of stay: %B %Y", errors="coerce"
        # )
        # self.df.dropna(subset=["date"], inplace=True)

        # Group the data by year and calculate the average rating for each year
        yearly_ratings = (
            self.df.groupby(self.df["date"].dt.year)["rating"].mean().reset_index()
        )

        fig = px.line(
            yearly_ratings,
            x="date",
            y="rating",
            title="Average Ratings Over Years",
            labels={"rating": "Average Rating"},
        )

        fig.update_xaxes(
            title_text="Year",
        )
        fig.update_traces(mode="lines+markers")

        st.plotly_chart(fig, use_container_width=True)

    def plot_near_attractions_restaurants3(self):
        """
        This function plots the relationship between the number of nearby restaurants, attractions, and average ratings for the selected hotel.

        Returns:
            None
        """
        # Split the "near_attraction" column into separate columns for restaurants and attractions
        self.df["restaurants"] = (
            self.df["near_attractions"].str.extract(r"(\d+) Restaurants").astype(int)
        )
        self.df["attractions"] = (
            self.df["near_attractions"].str.extract(r"(\d+) Attractions").astype(int)
        )

        # Create bins for the number of restaurants and attractions
        restaurant_bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, float("inf")]
        attraction_bins = [0, 20, 40, 60, 80, 100, 120, 140, float("inf")]

        self.df["restaurants_bin"] = pd.cut(
            self.df["restaurants"],
            bins=restaurant_bins,
            labels=[
                "0-100",
                "101-200",
                "201-300",
                "301-400",
                "401-500",
                "501-600",
                "601-700",
                "701-800",
                "801-900",
                "900+",
            ],
            right=False,
        )
        self.df["attractions_bin"] = pd.cut(
            self.df["attractions"],
            bins=attraction_bins,
            labels=[
                "0-20",
                "21-40",
                "41-60",
                "61-80",
                "81-100",
                "101-120",
                "121-140",
                "140+",
            ],
            right=False,
        )

        # Calculate average ratings for each bin
        average_ratings_restaurants = (
            self.df.groupby("restaurants_bin")["rating"].mean().reset_index()
        )
        average_ratings_attractions = (
            self.df.groupby("attractions_bin")["rating"].mean().reset_index()
        )

        fig1 = px.line(
            average_ratings_restaurants,
            x="restaurants_bin",
            y="rating",
            title="Average Ratings vs. Number of Restaurants for all hotels",
            labels={
                "restaurants_bin": "Number of Restaurants",
                "rating": "Average Rating",
            },
        )

        fig2 = px.line(
            average_ratings_attractions,
            x="attractions_bin",
            y="rating",
            title="Average Ratings vs. Number of Attractions for all hotels",
            labels={
                "attractions_bin": "Number of Attractions",
                "rating": "Average Rating",
            },
        )

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1)

        with col2:
            st.plotly_chart(fig2)


    def plot_review_count_by_rating_box_whisker(self):
        """
        This function plots a box and whisker plot for review count by rating for the selected hotel.

        Returns:
            None
        """
        self.df['review_count'] = self.df['review_count'].fillna("0").astype(str).str.replace(',', '', regex=True).str.extract('(\d+)').astype(int)

        grouped_df = self.df.groupby("name", as_index=False).agg(
            {"review_count": "first", "hotel_average_ratings": "first"}
        )

        fig = px.box(
            grouped_df,
            x="hotel_average_ratings",
            y="review_count",
            title="Review Count by Hotel Ratings"
        )
        fig.update_layout(yaxis_title="Review Count", xaxis_title="Hotel Ratings")

        st.plotly_chart(fig, use_container_width=True)
