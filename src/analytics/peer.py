import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def load_ratios():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    conn.close()
    return df


def calculate_percentiles(df):

    numeric_cols = df.select_dtypes(include="number").columns

    results = []

    for col in numeric_cols:

        pct = df[col].rank(pct=True)

        temp = pd.DataFrame({
            "company_id": df["company_id"],
            "metric": col,
            "value": df[col],
            "percentile_rank": pct
        })

        results.append(temp)

    return pd.concat(results, ignore_index=True)


def save_percentiles(df):

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()


def run():

    ratios = load_ratios()

    percentiles = calculate_percentiles(ratios)

    save_percentiles(percentiles)

    print(percentiles.head())

    return percentiles


if __name__ == "__main__":
    run()