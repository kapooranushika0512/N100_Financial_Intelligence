import os
import sys

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dashboard.utils.db import (
    get_companies,
    get_latest_ratios,
    get_market_cap_latest,
    get_sectors,
)


def load_data():
    """Load and merge company financial ratios, market cap, sector, and profile datasets."""

    ratios = get_latest_ratios()
    market = get_market_cap_latest()
    sectors = get_sectors()
    companies = get_companies()

    ratios = ratios.drop(columns=["id"], errors="ignore")
    market = market.drop(columns=["id"], errors="ignore")
    sectors = sectors.drop(columns=["id"], errors="ignore")

    df = (
        ratios.merge(
            market,
            on="company_id",
            how="left",
            suffixes=("", "_market"),
        )
        .merge(
            sectors,
            on="company_id",
            how="left",
        )
        .merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left",
        )
    )

    return df


def calculate_fcf_yield(df):
    """Calculate the free cash flow yield percentage for each company."""

    df["free_cash_flow_cr"] = pd.to_numeric(
        df["free_cash_flow_cr"],
        errors="coerce",
    )

    df["market_cap_crore"] = pd.to_numeric(
        df["market_cap_crore"],
        errors="coerce",
    )

    df["fcf_yield_pct"] = (df["free_cash_flow_cr"] / df["market_cap_crore"]) * 100

    return df


def calculate_sector_pe(df):
    """Calculate median P/E ratio for each broad sector and merge it into the dataframe."""

    df["pe_ratio"] = pd.to_numeric(
        df["pe_ratio"],
        errors="coerce",
    )

    sector_median = (
        df.groupby("broad_sector")["pe_ratio"]
        .median()
        .reset_index()
        .rename(
            columns={
                "pe_ratio": "sector_median_pe",
            }
        )
    )

    df = df.merge(
        sector_median,
        on="broad_sector",
        how="left",
    )

    return df


def assign_flag(df):
    """Assign valuation assessment flags based on comparison against sector median P/E."""

    def flag(row):

        pe = row["pe_ratio"]
        median = row["sector_median_pe"]

        if pd.isna(pe) or pd.isna(median):
            return "Unknown"

        if pe > median * 1.5:
            return "Caution"

        elif pe < median * 0.7:
            return "Discount"

        else:
            return "Fair"

    df["valuation_flag"] = df.apply(
        flag,
        axis=1,
    )

    return df


def export_results(df):
    """Export valuation analysis summary to Excel and CSV output files."""

    os.makedirs(
        "output",
        exist_ok=True,
    )

    df.to_excel(
        "output/valuation_summary.xlsx",
        index=False,
    )

    df[
        [
            "company_id",
            "company_name",
            "broad_sector",
            "pe_ratio",
            "sector_median_pe",
            "fcf_yield_pct",
            "valuation_flag",
        ]
    ].to_csv(
        "output/valuation_flags.csv",
        index=False,
    )

    print("✅ Files generated successfully.")
    print("📄 output/valuation_summary.xlsx")
    print("📄 output/valuation_flags.csv")


if __name__ == "__main__":

    df = load_data()

    df = calculate_fcf_yield(df)

    df = calculate_sector_pe(df)

    df = assign_flag(df)

    export_results(df)

    print(df.head())
