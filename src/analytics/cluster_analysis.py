import warnings

warnings.filterwarnings("ignore")

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.dashboard.utils.db import (
    get_analysis,
    get_companies,
    get_latest_ratios,
    get_sectors,
)

# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "output"
REPORT_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# KPI COLUMNS
# ---------------------------------------------------

KPI_COLUMNS = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
    "compounded_sales_growth",
    "interest_coverage",
    "asset_turnover",
    "net_profit_margin_pct",
    "book_value_per_share",
    "earnings_per_share",
]


def load_data():
    """Load and merge financial metrics across companies, ratios, sectors, and analysis."""

    companies = get_companies()[["id", "company_name"]].copy()

    ratios = get_latest_ratios().copy()

    sectors = get_sectors()[["company_id", "broad_sector"]].copy()

    analysis = get_analysis()[
        [
            "company_id",
            "compounded_sales_growth",
        ]
    ].copy()

    analysis["compounded_sales_growth"] = pd.to_numeric(
        analysis["compounded_sales_growth"], errors="coerce"
    )

    df = companies.merge(ratios, left_on="id", right_on="company_id", how="left")

    df = df.merge(sectors, on="company_id", how="left")

    df = df.merge(analysis, on="company_id", how="left")

    return df


def preprocess(df):
    """Preprocess financial KPI data by converting types and imputing missing values."""

    for col in KPI_COLUMNS:

        df[col] = pd.to_numeric(df[col], errors="coerce")

        sector_median = df.groupby("broad_sector")[col].transform("median")

        df[col] = df[col].fillna(sector_median)

        median = df[col].median()

        if pd.isna(median):
            median = 0

        df[col] = df[col].fillna(median)

    return df


def generate_correlation_heatmap(df):
    """Generate and save a correlation heatmap image for financial KPIs."""

    correlation = df[KPI_COLUMNS].corr()

    plt.figure(figsize=(12, 10))

    sns.heatmap(correlation, annot=True, cmap="RdYlGn", fmt=".2f", linewidths=0.5)

    plt.title("Financial KPI Correlation Heatmap")

    plt.tight_layout()

    plt.savefig(REPORT_DIR / "correlation_heatmap.png", dpi=300)

    plt.close()

    print("✓ correlation_heatmap.png created")


def generate_portfolio_statistics(df):
    """Calculate and export statistical summaries of portfolio KPIs to CSV."""

    stats = []

    for col in KPI_COLUMNS:

        values = df[col]

        stats.append(
            {
                "Metric": col,
                "Mean": values.mean(),
                "Median": values.median(),
                "Std": values.std(),
                "Min": values.min(),
                "P25": values.quantile(0.25),
                "P50": values.quantile(0.50),
                "P75": values.quantile(0.75),
                "Max": values.max(),
            }
        )

    portfolio = pd.DataFrame(stats).round(2)

    portfolio.to_csv(OUTPUT_DIR / "portfolio_stats.csv", index=False)

    print("✓ portfolio_stats.csv created")


def detect_outliers(df):
    """Identify sector-relative metric outliers and save the report to CSV."""

    outliers = []

    for sector in df["broad_sector"].dropna().unique():

        sector_df = df[df["broad_sector"] == sector].copy()

        for col in KPI_COLUMNS:

            mean = sector_df[col].mean()

            std = sector_df[col].std()

            if std == 0 or pd.isna(std):
                continue

            z = ((sector_df[col] - mean) / std).abs()

            temp = sector_df[z > 3].copy()

            if temp.empty:
                continue

            temp["metric"] = col

            temp["z_score"] = z[z > 3]

            outliers.append(temp)

    if outliers:

        result = pd.concat(outliers, ignore_index=True)

    else:

        result = pd.DataFrame()

    result.to_csv(OUTPUT_DIR / "outlier_report.csv", index=False)

    print("✓ outlier_report.csv created")


def main():
    """Execute the financial intelligence analysis workflow."""

    print("=" * 60)

    print("Financial Intelligence - Day 37")

    print("=" * 60)

    print("\nLoading data...")

    df = load_data()

    print(f"Companies Loaded : {len(df)}")

    print("\nPreprocessing data...")

    df = preprocess(df)

    print("\nGenerating correlation heatmap...")

    generate_correlation_heatmap(df)

    print("\nGenerating portfolio statistics...")

    generate_portfolio_statistics(df)

    print("\nDetecting outliers...")

    detect_outliers(df)

    print("\n" + "=" * 60)

    print("Day 37 Completed Successfully!")

    print("=" * 60)

    print("\nGenerated Outputs:")

    print(f"✓ {REPORT_DIR / 'correlation_heatmap.png'}")

    print(f"✓ {OUTPUT_DIR / 'portfolio_stats.csv'}")

    print(f"✓ {OUTPUT_DIR / 'outlier_report.csv'}")


if __name__ == "__main__":

    main()
