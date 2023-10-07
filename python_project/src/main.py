import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sentiment_analysis.sa_vader import SentimentAnalyzer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
stopwords = set(STOPWORDS)

# Create a Streamlit app
st.set_page_config(page_title="Streamlit App with Side Menu", layout="wide")

# Create a sidebar menu with radio buttons
st.sidebar.title("Menu")

selected_option = st.sidebar.radio("Select an option", ("Home", "EDA", "Sentiment Analysis", "Dataset"))

# Display a welcome message on the main page
st.title("Welcome")
st.subheader("This is where Hotel Sentiment Analysis and Data Visualization begin.")

uploaded_file = st.file_uploader("Upload a CSV file to Begin", type=["csv", "xls", "json"])
st.write("Navigation is made possible with Menu Panel (Top LEFT of the Page)")

# Main app logic
if uploaded_file is not None:
    # Get the file extension
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "csv":
        data = pd.read_csv(uploaded_file)
        # Perform data analysis or visualization for CSV data here

    elif file_extension in ("xls", "xlsx"):
        data = pd.read_excel(uploaded_file, engine="openpyxl")  # Use 'xlrd' for XLS files
        # Perform data analysis or visualization for Excel data here

    elif file_extension == "json":
        data = pd.read_json(uploaded_file)
        # Perform data analysis or visualization for JSON data here

    # Depending on the selected sidebar option, show different content
    if selected_option == "EDA":
        st.title("Exploratory Data Analysis")
        # Add code for EDA here

    elif selected_option == "Sentiment Analysis":

        name = 'The Ritz-Carlton, Millenia Singapore'
        analyzer = SentimentAnalyzer(data, name)
        df = analyzer.analyze_sentiment()

        st.title(f"Sentiment Analysis for {name}")
        chart1,chart2 = st.columns(2)

        with chart1:
            st.subheader("Sentiment Histogram")
            sentiment_counts = df['sentiment']
            fig = px.histogram(df, x='sentiment')
            histogram = go.Figure(fig)
            st.plotly_chart(histogram, use_container_width=True)
        with chart2:
            st.subheader("Sentiment Pie chart")
            sentiment_counts = df['sentiment']
            fig = px.pie(df, names='sentiment', title='Pie chart for sentiment analysis', hole = 0.3)
            pie = go.Figure(fig)
            st.plotly_chart(pie, use_container_width=True)

        st.subheader(f'Word Cloud for {name}')
        text = ''.join(comment for comment in df['comment_content'])
        word_cloud = WordCloud(collocations = False, background_color = 'white').generate(text)

        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

    elif selected_option == "Dataset":
        st.title("Dataset")
        st.write(data)

else:
    st.warning("Please upload a CSV, XLS, or JSON file.")
    
