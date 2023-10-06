import pandas as pd
import streamlit as st

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
        st.title("Sentiment Analysis")
        # Add code for sentiment analysis here

    elif selected_option == "Dataset":
        st.title("Dataset")
        st.write(data)

else:
    st.warning("Please upload a CSV, XLS, or JSON file.")
    
