import re
from pathlib import Path

import pandas as pd

from src.dashboard.utils.db import (
    get_analysis,
    get_ratios,
)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

PATTERN = re.compile(r"(\d+)\s*Years?\s*:?\s*([\d.]+)%", re.IGNORECASE)

TARGET_COLUMNS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]


def parse_value(text):
    """
    Extract:
    10 Years: 21%

    returns

    period = 10
    value = 21
    """

    if pd.isna(text):
        return None

    match = PATTERN.search(str(text))

    if match:
        return int(match.group(1)), float(match.group(2))

    return None


def parse_analysis(df):

    parsed_rows = []
    failures = []

    for _, row in df.iterrows():

        company = row["company_id"]

        for metric in TARGET_COLUMNS:

            result = parse_value(row[metric])

            if result:

                years, value = result

                parsed_rows.append(
                    {
                        "company_id": company,
                        "metric_type": metric,
                        "period_years": years,
                        "value_pct": value,
                    }
                )

            else:

                failures.append(
                    {
                        "company_id": company,
                        "metric_type": metric,
                        "raw_text": row[metric],
                    }
                )

    parsed = pd.DataFrame(parsed_rows)
    failed = pd.DataFrame(failures)

    return parsed, failed


def validate_against_ratios(parsed_df):

    ratios = get_ratios()

    ratio_map = {
        "compounded_sales_growth": "sales_growth_pct",
        "compounded_profit_growth": "profit_growth_pct",
        "roe": "roe_percentage",
    }

    review = []

    latest = (
        ratios.sort_values("year")
        .groupby("company_id")
        .tail(1)
    )

    for metric, ratio_col in ratio_map.items():

        if ratio_col not in latest.columns:
            continue

        subset = parsed_df[
            parsed_df.metric_type == metric
        ]

        merged = subset.merge(
            latest[["company_id", ratio_col]],
            on="company_id",
            how="left",
        )

        merged["difference"] = (
            merged["value_pct"] - merged[ratio_col]
        ).abs()

        review.append(
            merged[
                merged["difference"] > 5
            ]
        )

    if review:

        return pd.concat(review)

    return pd.DataFrame()


def main():

    print("Loading analysis...")

    analysis = get_analysis()

    print(f"Rows: {len(analysis)}")

    parsed, failed = parse_analysis(analysis)

    parsed.to_csv(
        OUTPUT_DIR / "analysis_parsed.csv",
        index=False,
    )

    failed.to_csv(
        OUTPUT_DIR / "parse_failures.csv",
        index=False,
    )

    review = validate_against_ratios(parsed)

    if len(review):

        review.to_csv(
            OUTPUT_DIR / "cagr_validation_review.csv",
            index=False,
        )

    print("Done")
    print(f"Parsed rows : {len(parsed)}")
    print(f"Failures    : {len(failed)}")
    print(f"Review rows : {len(review)}")


if __name__ == "__main__":
    main()