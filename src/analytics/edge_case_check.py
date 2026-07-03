import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

companies = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

merged = ratios.merge(
    companies[
        [
            "id",
            "roe_percentage",
            "roce_percentage"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)

log = open(
    "output/ratio_edge_cases.log",
    "w"
)

log.write("SPRINT 2 EDGE CASE REVIEW\n")
log.write("=" * 60 + "\n\n")

for _, row in merged.iterrows():

    # ROE check
    if (
        pd.notna(row["roe_percentage"])
        and pd.notna(row["return_on_equity_pct"])
    ):

        diff = abs(
            row["return_on_equity_pct"]
            - row["roe_percentage"]
        )

        if diff > 5:

            log.write(
                f"{row['company_id']} {row['year']} | "
                f"ROE Difference={diff:.2f}% | "
                f"Category: Version Difference\n"
            )

    # ROCE check
    if (
        pd.notna(row["roce_percentage"])
        and pd.notna(row["return_on_equity_pct"])
    ):

        diff = abs(
            row["return_on_equity_pct"]
            - row["roce_percentage"]
        )

        if diff > 5:

            log.write(
                f"{row['company_id']} {row['year']} | "
                f"ROCE Difference={diff:.2f}% | "
                f"Category: Formula Difference\n"
            )

financials = [
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "KOTAKBANK",
    "AXISBANK",
    "INDUSINDBK",
    "BANKBARODA",
    "PNB",
    "IDBI",
    "FEDERALBNK",
    "AUBANK",
    "BAJFINANCE",
    "BAJAJFINSV",
    "SBICARD",
    "ICICIPRULI",
    "HDFCLIFE",
    "SBILIFE",
    "LICI",
    "PFC"
]

log.write("\n")
log.write("=" * 60 + "\n")
log.write("Financial Sector Carve-out\n")
log.write("=" * 60 + "\n")

for company in financials:

    log.write(
        f"{company}: High leverage warning suppressed.\n"
    )

log.close()

conn.close()

print("ratio_edge_cases.log created successfully")