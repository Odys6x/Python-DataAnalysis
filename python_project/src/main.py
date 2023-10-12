import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sentiment_analysis.sa_vader import SentimentAnalyzer
from data_cleaning.cleaning import DataCleaning
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys
import streamlit.web.cli as stcli
from streamlit import runtime


def main():
    # Create a Streamlit app
    st.set_page_config(page_title="Streamlit App with Side Menu", layout="wide")

    # Create a sidebar menu with radio buttons
    st.sidebar.title("Menu")

    selected_option = st.sidebar.radio(
        "Select an option", ("Home", "EDA", "Sentiment Analysis", "Dataset")
    )

    # Display a welcome message on the main page
    st.title("Welcome")
    st.subheader("This is where Hotel Sentiment Analysis and Data Visualization begin.")

    uploaded_file = st.file_uploader(
        "Upload a CSV file to Begin", type=["csv", "xls", "json"]
    )
    st.write("Navigation is made possible with Menu Panel (Top LEFT of the Page)")

    # Main app logic
    if uploaded_file is not None:
        # Get the file extension
        file_extension = uploaded_file.name.split(".")[-1].lower()

        match file_extension:
            case "csv":
                data = pd.read_csv(uploaded_file)
                data_cleaner = DataCleaning()
                data = data_cleaner.cleaned_df(data)

            case "xls" | "xlsx":
                data = pd.read_excel(uploaded_file, engine="openpyxl")
            case "json":
                data = pd.read_json(uploaded_file)

        unique_values = data["name"].unique()
        # selected name of hotel
        selected_name = st.selectbox("Select a value:", unique_values)

        # Depending on the selected sidebar option, show different content
        match selected_option:
            case "EDA":
                st.title("Exploratory Data Analysis")
                # Add code for EDA here

            case "Sentiment Analysis":
                analyzer = SentimentAnalyzer(data, selected_name)
                df = analyzer.analyze_sentiment()

                st.title(f"Sentiment Analysis for {selected_name}")
                chart1, chart2 = st.columns(2)

                with chart1:
                    st.subheader("Sentiment Histogram")
                    sentiment_counts = df["sentiment"]
                    fig = px.histogram(df, x="sentiment")
                    fig.update_xaxes(
                        categoryorder="array", categoryarray=["neg", "neu", "pos"]
                    )
                    histogram = go.Figure(fig)
                    st.plotly_chart(histogram, use_container_width=True)
                with chart2:
                    st.subheader("Sentiment Pie chart")
                    sentiment_counts = df["sentiment"]
                    fig = px.pie(
                        df,
                        names="sentiment",
                        title="Pie chart for sentiment analysis",
                        hole=0.3,
                    )
                    pie = go.Figure(fig)
                    st.plotly_chart(pie, use_container_width=True)

                st.subheader(f"Word Cloud for {selected_name}")
                text = "".join(comment for comment in df["comment_content"])
                word_cloud = WordCloud(
                    collocations=False, background_color="white", width=800, height=400
                ).generate(text)

                plt.imshow(word_cloud, interpolation="bilinear")
                plt.axis("off")
                st.pyplot(plt)

            case "Dataset":
                st.title("Dataset")
                selected_row = data[data["name"] == selected_name]
                st.write(selected_row)

    else:
        st.warning("Please upload a CSV, XLS, or JSON file.")


if __name__ == "__main__":
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
