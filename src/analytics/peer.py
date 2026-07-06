import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def load_data():
    ratios = pd.read_excel("data/supporting/financial_ratios.xlsx")
    analysis = pd.read_excel("data/raw/analysis.xlsx", header=1)
    peers = pd.read_excel("data/supporting/peer_groups.xlsx")
    sectors = pd.read_excel("data/supporting/sectors.xlsx")

    # Remove duplicate id columns before merging
    analysis = analysis.drop(columns=["id"], errors="ignore")
    peers = peers.drop(columns=["id"], errors="ignore")
    sectors = sectors.drop(columns=["id"], errors="ignore")

    # Keep only required sector columns
    sectors = sectors[
        [
            "company_id",
            "broad_sector",
            "sub_sector",
            "market_cap_category",
        ]
    ]

    # Merge datasets
    df = ratios.merge(
        analysis,
        on="company_id",
        how="left"
    )

    df = df.merge(
        peers,
        on="company_id",
        how="left"
    )

    df = df.merge(
        sectors,
        on="company_id",
        how="left"
    )

    return df


def percentile(series, reverse=False):
    series = pd.to_numeric(series, errors="coerce")

    pct = series.rank(
        method="average",
        pct=True
    )

    if reverse:
        pct = 1 - pct

    return pct.round(4)


def compute_percentiles(df):

    metrics = {
        "return_on_equity_pct": False,
        "net_profit_margin_pct": False,
        "operating_profit_margin_pct": False,
        "debt_to_equity": True,
        "interest_coverage": False,
        "asset_turnover": False,
        "free_cash_flow_cr": False,
        "compounded_sales_growth": False,
        "compounded_profit_growth": False,
    }

    rows = []

    for peer_name, group in df.groupby("peer_group_name", dropna=False):

        if pd.isna(peer_name):
            continue

        for metric, reverse in metrics.items():

            if metric not in group.columns:
                continue

            pct = percentile(group[metric], reverse)

            for idx, row in group.iterrows():

                rows.append(
                    {
                        "company_id": row["company_id"],
                        "peer_group_name": peer_name,
                        "metric": metric,
                        "value": row[metric],
                        "percentile_rank": pct.loc[idx],
                        "year": row["year"],
                    }
                )

    return pd.DataFrame(rows)


def save_sqlite(df):

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()


def run():

    df = load_data()

    result = compute_percentiles(df)

    save_sqlite(result)

    print(result.head())

    return result


if __name__ == "__main__":
    run()