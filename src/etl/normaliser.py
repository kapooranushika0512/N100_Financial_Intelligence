import pandas as pd


def normalize_ticker(value):
    """Convert company ticker string to uppercase and strip whitespace."""

    if pd.isna(value):
        return None

    return str(value).strip().upper()


def normalize_year(value):
    """Standardize financial year value as a clean string."""

    if pd.isna(value):
        return None

    return str(value).strip()


def normalize_columns(df):
    """Normalize DataFrame column names to lower_snake_case format."""

    df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(" ", "_")

    return df
