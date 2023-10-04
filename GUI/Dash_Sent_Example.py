import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from dateutil import parser

# Create a Streamlit web app
st.title("Hotel Review Sentiment Analysis Dashboard")

# Upload a CSV file containing hotel reviews
uploaded_file = st.file_uploader("Upload a CSV file with hotel reviews", type=["csv", "xls", "json"])


# Function to perform sentiment analysis and create visualizations
def perform_sentiment_analysis(data):
    # Ensure the 'reviews.text' column contains only string values
    data['reviews.text'] = data['reviews.text'].astype(str)

    # Parse the 'reviews.date' column as datetime
    data['reviews.date'] = data['reviews.date'].apply(lambda x: parser.isoparse(x) if isinstance(x, str) else x)

    # Create a new column for sentiment analysis
    data['Sentiment'] = data['reviews.text'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Define a threshold for sentiment categorization
    threshold = 0.1  # Adjust this threshold as needed

    # Categorize sentiment as positive, negative, or neutral
    data['Sentiment_Label'] = data['Sentiment'].apply(
        lambda x: 'Positive' if x > threshold else ('Negative' if x < -threshold else 'Neutral'))

    chart1, chart2 = st.columns(2)

    with chart1:
        # Sentiment distribution donut chart (Plotly)
        st.subheader("Sentiment Categories")
        sentiment_counts = data['Sentiment_Label'].value_counts()
        donut_fig = go.Figure(data=[go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values, hole=0.3)])
        st.plotly_chart(donut_fig, use_container_width=True)

    with chart2:
        # Sentiment vs. Review Ratings Scatterplot
        st.subheader("Sentiment vs. Review Ratings Scatterplot")
        scatter_fig = px.scatter(data, x='reviews.rating', y='Sentiment', color='Sentiment_Label',
                                 title='Sentiment vs. Review Ratings Scatterplot')
        st.plotly_chart(scatter_fig, use_container_width=True)

    chart1, chart2 = st.columns(2)
    with chart1:
        # Average Sentiment by Province Bar Chart
        st.subheader("Average Sentiment by Province")
        avg_sentiment_by_province = data.groupby('province')['Sentiment'].mean().reset_index()
        bar_fig = px.bar(avg_sentiment_by_province, x='province', y='Sentiment',
                         title='Average Sentiment by Province')
        st.plotly_chart(bar_fig, use_container_width=True)

    with chart2:
        # Stream graph for Sentiment Over Time
        st.subheader("Sentiment Over Time (Stream Graph)")
        data['Year'] = data['reviews.date'].dt.year
        sentiment_over_time = data.groupby(['Year', 'Sentiment_Label']).size().reset_index(name='Count')
        stream_fig = px.area(sentiment_over_time, x='Year', y='Count', color='Sentiment_Label',
                             title='Sentiment Over Time (Stream Graph)',
                             labels={'Year': 'Year', 'Count': 'Count'},
                             category_orders={"Sentiment_Label": ["Positive", "Negative", "Neutral"]})
        st.plotly_chart(stream_fig, use_container_width=True)

    # Word cloud
    st.subheader("Word Cloud")
    reviews = ' '.join(data['reviews.text'])

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400).generate(reviews)

    # Display the word cloud using Matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    st.pyplot(plt)


# Main app logic
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Perform sentiment analysis and create visualizations
    perform_sentiment_analysis(data)

    # Display the counts of each sentiment category
    st.subheader("Sentiment Category Counts")
    sentiment_counts = data['Sentiment_Label'].value_counts()
    st.write(sentiment_counts)

    # Display all the analyzed data
    st.subheader("All Analyzed Data")
    st.write(data)
else:
    st.warning("Please upload a CSV file with hotel reviews.")
