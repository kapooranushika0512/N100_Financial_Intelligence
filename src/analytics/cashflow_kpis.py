import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():
    """Load financial datasets from the SQLite database."""

    conn = sqlite3.connect(DB_PATH)

    profit = pd.read_sql("SELECT * FROM profitandloss", conn)

    cash = pd.read_sql("SELECT * FROM cashflow", conn)

    balance = pd.read_sql("SELECT * FROM balancesheet", conn)

    ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

    sectors = pd.read_sql(
        """
        SELECT
            company_id,
            broad_sector
        FROM sectors
        """,
        conn,
    )

    conn.close()

    return (profit, cash, balance, ratios, sectors)


def prepare_dataframe():
    """Merge and clean financial tables into a unified dataframe."""

    profit, cash, balance, ratios, sectors = load_data()

    # Remove duplicate primary keys before merging
    profit = profit.drop(columns=["id"], errors="ignore")
    cash = cash.drop(columns=["id"], errors="ignore")
    balance = balance.drop(columns=["id"], errors="ignore")
    ratios = ratios.drop(columns=["id"], errors="ignore")
    sectors = sectors.drop(columns=["id"], errors="ignore")

    # Merge all tables
    df = (
        profit.merge(cash, on=["company_id", "year"], how="inner")
        .merge(balance, on=["company_id", "year"], how="inner")
        .merge(ratios, on=["company_id", "year"], how="inner")
        .merge(sectors, on="company_id", how="left")
    )

    df.rename(columns={"broad_sector": "sector"}, inplace=True)

    # Extract numeric year for sorting
    df["year_num"] = df["year"].astype(str).str.extract(r"(\d{4})")[0].astype(int)

    # Remove duplicate company-year records if present
    df = (
        df.sort_values(["company_id", "year_num"])
        .drop_duplicates(subset=["company_id", "year_num"], keep="last")
        .reset_index(drop=True)
    )

    return df


def cfo_quality_label(score):
    """Categorize the CFO quality score into a descriptive label."""

    if pd.isna(score):
        return "Unknown"

    if score > 1:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_label(value):
    """Categorize CapEx intensity percentage into an asset class label."""

    if pd.isna(value):
        return "Unknown"

    if value < 3:
        return "Asset Light"

    if value <= 8:
        return "Moderate"

    return "Capital Intensive"


def free_cash_flow(cfo, capex):
    """Calculate the total free cash flow."""
    return cfo + capex


def cfo_quality_score(cfo, pat):
    """Determine the cash flow quality score based on operating cash and net profit."""
    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio >= 1:
        return "High Quality"
    elif ratio >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"


def capex_intensity(capex, revenue):
    """Evaluate capital intensity relative to company revenue."""
    if revenue == 0:
        return None

    ratio = abs(capex) / revenue

    if ratio < 0.05:
        return "Asset Light"
    elif ratio < 0.15:
        return "Moderate"
    else:
        return "Capital Intensive"


def fcf_conversion_rate(fcf, pat):
    """Calculate the free cash flow conversion rate percentage."""
    if pat == 0:
        return None

    return (fcf / pat) * 100


def calculate_cagr(values):
    """Calculate the compound annual growth rate for a series of values."""

    values = values.dropna()

    if len(values) < 2:
        return np.nan

    first = values.iloc[0]
    last = values.iloc[-1]

    years = len(values) - 1

    if years <= 0 or pd.isna(first) or pd.isna(last) or first <= 0 or last <= 0:
        return np.nan

    return round(
        (((last / first) ** (1 / years)) - 1) * 100,
        2,
    )


def calculate_kpis(df):
    """Compute cash flow key performance indicators and financial health flags."""

    df["cfo_quality_score"] = df["cash_from_operations_cr"] / df["net_profit"]

    df["cfo_quality_label"] = df["cfo_quality_score"].apply(cfo_quality_label)

    df["capex_intensity_pct"] = (abs(df["investing_activity"]) / df["sales"]) * 100

    df["capex_label"] = df["capex_intensity_pct"].apply(capex_label)

    df["fcf_conversion_pct"] = (df["free_cash_flow_cr"] / df["net_profit"]) * 100

    df = df.sort_values(["company_id", "year_num"])

    fcf_cagr = (
        df.groupby("company_id")["free_cash_flow_cr"]
        .apply(calculate_cagr)
        .reset_index()
    )

    fcf_cagr.columns = ["company_id", "fcf_cagr_5yr"]

    latest = df.sort_values("year_num").groupby("company_id").tail(1).copy()

    latest["distress_flag"] = (latest["operating_activity"] < 0) & (
        latest["financing_activity"] > 0
    )

    latest["previous_borrowings"] = (
        df.groupby("company_id")["borrowings"].shift(1).loc[latest.index]
    )

    latest["deleveraging_flag"] = (latest["financing_activity"] < 0) & (
        latest["borrowings"] < latest["previous_borrowings"]
    )

    latest = latest.merge(fcf_cagr, on="company_id", how="left")

    return latest


def export_results(latest):
    """Export cash flow intelligence reports and distress alerts to output files."""

    capital = pd.read_csv("output/capital_allocation.csv")

    capital["year_num"] = (
        capital["year"].astype(str).str.extract(r"(\d{4})").astype(int)
    )

    capital = capital.sort_values("year_num").groupby("company_id").tail(1)

    capital.rename(columns={"pattern_label": "capital_allocation_label"}, inplace=True)

    final = latest.merge(
        capital[["company_id", "capital_allocation_label"]], on="company_id", how="left"
    )

    final = final[
        [
            "company_id",
            "sector",
            "cfo_quality_score",
            "cfo_quality_label",
            "capex_intensity_pct",
            "capex_label",
            "fcf_cagr_5yr",
            "fcf_conversion_pct",
            "distress_flag",
            "deleveraging_flag",
            "capital_allocation_label",
        ]
    ]

    final = final.sort_values("company_id")

    final.to_excel(OUTPUT_DIR / "cashflow_intelligence.xlsx", index=False)

    alerts = latest[latest["distress_flag"]][
        [
            "company_id",
            "sector",
            "operating_activity",
            "financing_activity",
            "net_profit",
        ]
    ].copy()

    alerts.rename(
        columns={
            "operating_activity": "latest_cfo",
            "financing_activity": "latest_cff",
            "net_profit": "latest_pat",
        },
        inplace=True,
    )

    alerts.to_csv(OUTPUT_DIR / "distress_alerts.csv", index=False)

    print("\nCash Flow Intelligence Created")

    print("Companies :", len(final))

    print("Distress Alerts :", len(alerts))

    return final


def main():
    """Execute the main cash flow analysis and report generation workflow."""

    print("\nLoading financial data...")

    df = prepare_dataframe()

    print("Calculating cash flow KPIs...")

    latest = calculate_kpis(df)

    print("Exporting outputs...")

    final = export_results(latest)

    print("\nPreview:\n")

    print(final.head(10))

    print("\nDone.")


if __name__ == "__main__":
    main()
