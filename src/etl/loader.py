import pandas as pd
from pathlib import Path

from normaliser import (
    normalize_ticker,
    normalize_year,
    normalize_columns
)

RAW_PATH = Path("data/raw")
SUPPORTING_PATH = Path("data/supporting")


def load_excel(file_path, header_row):
    """
    Load and clean a single Excel file
    """

    try:
        df = pd.read_excel(file_path, header=header_row)

        # normalize column names
        df = normalize_columns(df)

        # normalize company ids
        if "company_id" in df.columns:
            df["company_id"] = df["company_id"].apply(normalize_ticker)

        # normalize year column
        if "year" in df.columns:
            df["year"] = df["year"].apply(normalize_year)

        print(f"Loaded {file_path.name}: {df.shape}")

        return df

    except Exception as e:
        print(f"Error loading {file_path.name}: {e}")
        return None


def load_all_files():
    """
    Load all datasets
    """

    datasets = {}

    print("\nCORE FILES")
    print("-" * 40)

    for file in RAW_PATH.glob("*.xlsx"):
        datasets[file.stem] = load_excel(
            file,
            header_row=1
        )

    print("\nSUPPORTING FILES")
    print("-" * 40)

    for file in SUPPORTING_PATH.glob("*.xlsx"):
        datasets[file.stem] = load_excel(
            file,
            header_row=0
        )

    return datasets


def print_summary(datasets):

    print("\nSummary")
    print("-" * 40)

    for name, df in datasets.items():

        if df is not None:
            print(f"{name}: {len(df)} rows")
        else:
            print(f"{name}: FAILED")


if __name__ == "__main__":

    datasets = load_all_files()

    print_summary(datasets)