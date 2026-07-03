import sqlite3
import pandas as pd

from src.analytics.ratios import *
from src.analytics.cashflow_kpis import *

DB = "db/nifty100.db"


profit = pd.read_excel(
    "data/raw/profitandloss.xlsx",
    header=1
)

balance = pd.read_excel(
    "data/raw/balancesheet.xlsx",
    header=1
)

cash = pd.read_excel(
    "data/raw/cashflow.xlsx",
    header=1
)


df = (
    profit
    .merge(
        balance,
        on=["company_id","year"],
        how="inner"
    )
    .merge(
        cash,
        on=["company_id","year"],
        how="inner"
    )
)


rows = []

for _, r in df.iterrows():

    npm = net_profit_margin(
        r.net_profit,
        r.sales
    )

    opm = operating_profit_margin(
        r.operating_profit,
        r.sales
    )

    roe = return_on_equity(
        r.net_profit,
        r.equity_capital,
        r.reserves
    )

    de = debt_to_equity(
        r.borrowings,
        r.equity_capital,
        r.reserves
    )

    icr = interest_coverage(
        r.operating_profit,
        r.other_income,
        r.interest
    )

    at = asset_turnover(
        r.sales,
        r.total_assets
    )

    fcf = free_cash_flow(
        r.operating_activity,
        r.investing_activity
    )

    capex = capex_intensity(
        r.investing_activity,
        r.sales
    )

    rows.append({

        "company_id":r.company_id,

        "year":r.year,

        "net_profit_margin_pct":npm,

        "operating_profit_margin_pct":opm,

        "return_on_equity_pct":roe,

        "debt_to_equity":de,

        "interest_coverage":icr,

        "asset_turnover":at,

        "free_cash_flow_cr":fcf,

        "capex_cr":capex,

        "earnings_per_share":r.eps,

        "book_value_per_share":
        (
            (r.equity_capital+r.reserves)/r.equity_capital
            if r.equity_capital>0
            else None
        ),

        "dividend_payout_ratio_pct":
        r.dividend_payout,

        "total_debt_cr":
        r.borrowings,

        "cash_from_operations_cr":
        r.operating_activity

    })


ratio_df = pd.DataFrame(rows)


conn = sqlite3.connect(DB)

conn.execute(
    "DELETE FROM financial_ratios"
)

ratio_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="append",
    index=False
)

conn.commit()

print(
    f"Inserted {len(ratio_df)} rows into financial_ratios"
)

conn.close()