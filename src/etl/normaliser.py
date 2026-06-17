import pandas as pd


def normalize_ticker(value):
    """
    Convert company tickers to uppercase and remove spaces.
    Example: abb -> ABB
    """

    if pd.isna(value):
        return None

    return str(value).strip().upper()


def normalize_year(value):
    """
    Standardize year values.
    Examples:
    Dec 2012 -> Dec 2012
    Mar 2014 -> Mar 2014
    2020 -> 2020
    """

    if pd.isna(value):
        return None

    return str(value).strip()


def normalize_columns(df):
    """
    Standardize column names.
    """

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df