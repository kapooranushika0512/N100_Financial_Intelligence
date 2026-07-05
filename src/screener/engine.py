import sqlite3
import yaml
import pandas as pd
from src.screener.scoring import calculate_score
DB_PATH = "db/nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def load_ratios():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn,
    )

    conn.close()
    df = calculate_score(df)

    return df


def apply_filters(df, filters):

    result = df.copy()

    if "return_on_equity_pct" in result.columns:
        result = result[
            result["return_on_equity_pct"] >= filters["roe_min"]
        ]

    if "debt_to_equity" in result.columns:
        result = result[
            (result["debt_to_equity"] <= filters["debt_to_equity_max"])
            | (result["debt_to_equity"].isna())
        ]

    if "free_cash_flow_cr" in result.columns:
        result = result[
            result["free_cash_flow_cr"] >= filters["free_cash_flow_min"]
        ]

    if "asset_turnover" in result.columns:
        result = result[
            result["asset_turnover"] >= filters["asset_turnover_min"]
        ]

    return result


def add_composite_score(df):

    df = df.copy()

    score = 0

    if "return_on_equity_pct" in df.columns:
        score += df["return_on_equity_pct"].fillna(0)

    if "asset_turnover" in df.columns:
        score += df["asset_turnover"].fillna(0) * 20

    if "free_cash_flow_cr" in df.columns:
        score += (
            df["free_cash_flow_cr"]
            .fillna(0)
            .clip(lower=0)
            / 100
        )

    df["composite_quality_score"] = score

    return df.sort_values(
        "composite_quality_score",
        ascending=False
    )


def run():

    config = load_config()

    ratios = load_ratios()

    screened = apply_filters(
        ratios,
        config["filters"]
    )

    screened = add_composite_score(screened)

    print(screened.head())

    return screened


if __name__ == "__main__":
    run()