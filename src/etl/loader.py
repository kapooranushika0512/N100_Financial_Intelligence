from pathlib import Path

import pandas as pd
from normaliser import normalize_columns, normalize_ticker, normalize_year

RAW_PATH = Path("data/raw")
SUPPORTING_PATH = Path("data/supporting")


def load_excel(file_path, header_row):
    """Load, clean, and normalize a single Excel file with data quality filters."""

    try:
        df = pd.read_excel(file_path, header=header_row)

        df = normalize_columns(df)

        if "company_id" in df.columns:
            df["company_id"] = df["company_id"].apply(normalize_ticker)

        if "year" in df.columns:
            df["year"] = df["year"].apply(normalize_year)

        duplicates_removed = 0

        if "company_id" in df.columns and "year" in df.columns:
            before = len(df)

            df = df.drop_duplicates(subset=["company_id", "year"], keep="last")

            duplicates_removed = before - len(df)

        sales_removed = 0

        if file_path.stem == "profitandloss" and "sales" in df.columns:
            before = len(df)

            df = df[df["sales"] > 0]

            sales_removed = before - len(df)

        print(
            f"Loaded {file_path.name}: "
            f"{df.shape} "
            f"(removed {duplicates_removed} duplicates, "
            f"{sales_removed} invalid sales rows)"
        )

        return df

    except (FileNotFoundError, ValueError, KeyError, OSError) as e:
        print(f"Error loading {file_path.name}: {e}")
        return None


def load_all_files():
    """Load all core and supporting Excel datasets into a dictionary of DataFrames."""

    datasets = {}

    print("\nCORE FILES")
    print("-" * 40)

    for file in RAW_PATH.glob("*.xlsx"):
        datasets[file.stem] = load_excel(file, header_row=1)

    print("\nSUPPORTING FILES")
    print("-" * 40)

    for file in SUPPORTING_PATH.glob("*.xlsx"):
        datasets[file.stem] = load_excel(file, header_row=0)

    return datasets


def print_summary(datasets):
    """Print row counts and load status for each dataset in the dictionary."""

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
