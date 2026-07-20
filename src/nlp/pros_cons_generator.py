from pathlib import Path
import pandas as pd

from src.dashboard.utils.db import get_ratios

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

ANALYSIS_FILE = OUTPUT_DIR / "analysis_parsed.csv"


def latest_ratios():
    df = get_ratios()

    latest = (
        df.sort_values("year")
        .groupby("company_id")
        .tail(1)
        .reset_index(drop=True)
    )

    return latest


def load_growth_metrics():

    if not ANALYSIS_FILE.exists():
        return pd.DataFrame()

    growth = pd.read_csv(ANALYSIS_FILE)

    growth = (
        growth.sort_values("period_years", ascending=False)
        .groupby(["company_id", "metric_type"])
        .first()
        .reset_index()
    )

    return growth


def add(items, company, typ, reason, confidence):
    items.append(
        {
            "company_id": company,
            "type": typ,
            "reason": reason,
            "confidence": confidence,
        }
    )


def generate():

    ratios = latest_ratios()
    growth = load_growth_metrics()

    rows = []

    for _, r in ratios.iterrows():

        company = r.company_id

        company_growth = growth[
            growth.company_id == company
        ]

        pros = 0
        cons = 0

        # -------------------------
        # ROE
        # -------------------------

        if r.return_on_equity_pct >= 20:
            add(
                rows,
                company,
                "Pro",
                f"High ROE ({r.return_on_equity_pct:.1f}%)",
                0.95,
            )
            pros += 1

        elif r.return_on_equity_pct < 10:
            add(
                rows,
                company,
                "Con",
                f"Low ROE ({r.return_on_equity_pct:.1f}%)",
                0.90,
            )
            cons += 1

        # -------------------------
        # Debt
        # -------------------------

        if r.debt_to_equity <= 0.5:
            add(
                rows,
                company,
                "Pro",
                "Low debt levels",
                0.90,
            )
            pros += 1

        elif r.debt_to_equity > 1:
            add(
                rows,
                company,
                "Con",
                "High debt levels",
                0.90,
            )
            cons += 1

        # -------------------------
        # Net Profit Margin
        # -------------------------

        if r.net_profit_margin_pct >= 15:
            add(
                rows,
                company,
                "Pro",
                "Healthy net profit margin",
                0.90,
            )
            pros += 1

        elif r.net_profit_margin_pct < 5:
            add(
                rows,
                company,
                "Con",
                "Weak profitability",
                0.85,
            )
            cons += 1

        # -------------------------
        # Operating Margin
        # -------------------------

        if r.operating_profit_margin_pct >= 20:
            add(
                rows,
                company,
                "Pro",
                "Strong operating margin",
                0.90,
            )
            pros += 1

        elif r.operating_profit_margin_pct < 10:
            add(
                rows,
                company,
                "Con",
                "Weak operating margin",
                0.85,
            )
            cons += 1

        # -------------------------
        # Interest Coverage
        # -------------------------

        if r.interest_coverage >= 5:
            add(
                rows,
                company,
                "Pro",
                "Comfortable interest coverage",
                0.90,
            )
            pros += 1

        elif r.interest_coverage < 2:
            add(
                rows,
                company,
                "Con",
                "Low interest coverage",
                0.90,
            )
            cons += 1

        # -------------------------
        # Free Cash Flow
        # -------------------------

        if r.free_cash_flow_cr > 0:
            add(
                rows,
                company,
                "Pro",
                "Positive free cash flow",
                0.85,
            )
            pros += 1

        else:
            add(
                rows,
                company,
                "Con",
                "Negative free cash flow",
                0.90,
            )
            cons += 1

        # -------------------------
        # Asset Turnover
        # -------------------------

        if r.asset_turnover >= 1:
            add(
                rows,
                company,
                "Pro",
                "Efficient asset utilization",
                0.80,
            )
            pros += 1

        # ==================================================
        # NLP Growth Metrics (Day 29 Integration)
        # ==================================================

        # Sales CAGR

        sales = company_growth[
            company_growth.metric_type == "compounded_sales_growth"
        ]

        if not sales.empty:

            value = sales.iloc[0]["value_pct"]

            if value >= 15:
                add(
                    rows,
                    company,
                    "Pro",
                    f"Strong sales CAGR ({value:.1f}%)",
                    0.95,
                )
                pros += 1

            elif value < 5:
                add(
                    rows,
                    company,
                    "Con",
                    f"Weak sales growth ({value:.1f}%)",
                    0.90,
                )
                cons += 1

        # Profit CAGR

        profit = company_growth[
            company_growth.metric_type == "compounded_profit_growth"
        ]

        if not profit.empty:

            value = profit.iloc[0]["value_pct"]

            if value >= 15:
                add(
                    rows,
                    company,
                    "Pro",
                    f"Strong profit CAGR ({value:.1f}%)",
                    0.95,
                )
                pros += 1

            elif value < 5:
                add(
                    rows,
                    company,
                    "Con",
                    f"Weak profit growth ({value:.1f}%)",
                    0.90,
                )
                cons += 1

        # Historical ROE

        roe = company_growth[
            company_growth.metric_type == "roe"
        ]

        if not roe.empty:

            value = roe.iloc[0]["value_pct"]

            if value >= 20:
                add(
                    rows,
                    company,
                    "Pro",
                    f"Consistently high ROE ({value:.1f}%)",
                    0.90,
                )
                pros += 1

        # ==================================================
        # Fallback
        # ==================================================

        if pros == 0:
            add(
                rows,
                company,
                "Pro",
                "Stable financial performance",
                0.75,
            )

        if cons == 0:
            add(
                rows,
                company,
                "Con",
                "Requires further financial monitoring",
                0.75,
            )

    result = pd.DataFrame(rows)

    result.to_csv(
        OUTPUT_DIR / "pros_cons_generated.csv",
        index=False,
    )

    print(result.head())
    print()
    print(f"Generated {len(result)} insights")
    print(f"Companies : {result.company_id.nunique()}")


if __name__ == "__main__":
    generate()