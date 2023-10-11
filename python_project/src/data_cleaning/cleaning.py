import pandas as pd
import sys

sys.path.insert(0, "src/data_fetching")
from extraction import fetch_data


class DataCleaning:
    """
    A class for data cleaning operations on a DataFrame.

    Methods
    -------
    rename_column(df)
        Renames columns by replacing spaces with underscores and converting to lowercase.

    replace_not_ascii(df)
        Replaces non-ASCII characters in the 'comment_content' column with UTF-8 encoded characters.

    overall_experience(df)
        Extracts and converts values from the 'overall_experience' column.

    rename_hotel_class(df)
        Extracts and converts the 'hotel_class' column to a float.

    create_index(df)
        Adds an 'index' column to the DataFrame.

    cleaned_df()
        Performs a sequence of data cleaning operations on the DataFrame.

    Attributes
    ----------
    None
    """

    def rename_column(self, df):
        """
        Renames columns by replacing spaces with underscores and converting to lowercase.

        Parameters
        ----------
        df : pandas.DataFrame
            The input DataFrame.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with columns renamed.
        """
        df.columns = [x.replace(" ", "_") for x in df.columns]
        df.columns = [x.lower() for x in df.columns]
        return df

    def replace_not_ascii(self, df):
        """
        Replaces non-ASCII characters in the 'comment_content' column with UTF-8 encoded characters.

        Parameters
        ----------
        df : pandas.DataFrame
            The input DataFrame.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with 'comment_content' column modified.
        """
        df["comment_content"] = df["comment_content"].apply(
            lambda x: x.encode("ascii", "ignore").decode("utf-8")
        )
        return df

    def overall_experience(self, df):
        """
        Extracts and converts values from the 'overall_experience' column.

        Parameters
        ----------
        df : pandas.DataFrame
            The input DataFrame.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with 'overall_experience' column values processed.
        """
        df["overall_experience"] = df["overall_experience"].str.strip("[]")
        df["location"] = df["overall_experience"].str.split(",").str.get(0)
        df["cleanliness"] = df["overall_experience"].str.split(",").str.get(1)
        df["service"] = df["overall_experience"].str.split(",").str.get(2)
        df["value"] = df["overall_experience"].str.split(",").str.get(3)
        df["location"] = pd.to_numeric(df["location"])
        df["cleanliness"] = pd.to_numeric(df["cleanliness"])
        df["service"] = pd.to_numeric(df["service"])
        df["value"] = pd.to_numeric(df["value"])

        return df

    def rename_hotel_class(self, df):
        """
        Extracts and converts the 'hotel_class' column to a float.

        Parameters
        ----------
        df : pandas.DataFrame
            The input DataFrame.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with 'hotel_class' column values processed.
        """
        df["hotel_class"] = (
            df["hotel_class"].str.extract("(\d+\.\d+)", expand=False).astype(float)
        )
        return df

    def create_index(self, df):
        """
        Adds an 'index' column to the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The input DataFrame.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with an additional 'index' column.
        """
        df.insert(0, "index", df.index + 1)
        return df

    def cleaned_df(self, df):
        """
        Performs a sequence of data cleaning operations on the DataFrame.

        Returns
        -------
        pandas.DataFrame
            The cleaned DataFrame.
        """
        data_cleaner = DataCleaning()
        df = fetch_data()
        df = data_cleaner.rename_column(df)
        df = data_cleaner.replace_not_ascii(df)
        df = data_cleaner.overall_experience(df)
        df = data_cleaner.rename_hotel_class(df)
        df = data_cleaner.create_index(df)
        return df
