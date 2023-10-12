import pandas as pd


def fetch_data():
    """
    Load data from a CSV file.

    This function reads data from a CSV file located at 'data/raw/refined.csv'
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """
    filepath = "data/raw/refined.csv"
    df = pd.read_csv(filepath)
    return df
