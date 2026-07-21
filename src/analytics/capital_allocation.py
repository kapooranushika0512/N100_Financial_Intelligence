import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def sign(value):
    if pd.isna(value):
        return "0"
    return "+" if value >= 0 else "-"


def classify(cfo, cfi, cff):
    pattern = (cfo, cfi, cff)

    mapping = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "-"): "Shareholder Returns",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "+"): "Expansion Phase",
        ("-", "+", "-"): "Turnaround",
        ("-", "+", "+"): "Operating Stress",
        ("-", "-", "-"): "Cash Burn",
    }

    return mapping.get(pattern, "Mixed")


def main():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    conn.close()

    df["year_num"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{2})$")
        .astype(int)
    )

    df["year_num"] += 2000

    latest = (
        df.sort_values("year_num")
          .groupby("company_id")
          .tail(1)
          .copy()
    )

    latest["cfo_sign"] = latest["operating_activity"].apply(sign)
    latest["cfi_sign"] = latest["investing_activity"].apply(sign)
    latest["cff_sign"] = latest["financing_activity"].apply(sign)

    latest["pattern_label"] = latest.apply(
        lambda r: classify(
            r["cfo_sign"],
            r["cfi_sign"],
            r["cff_sign"],
        ),
        axis=1,
    )

    latest[
        [
            "company_id",
            "year",
            "cfo_sign",
            "cfi_sign",
            "cff_sign",
            "pattern_label",
        ]
    ].to_csv(
        "output/capital_allocation.csv",
        index=False,
    )

    print("Generated:", len(latest), "companies")


if __name__ == "__main__":
    main()