import streamlit as st
import pandas as pd

from utils.db import (
    get_latest_ratios,
    get_analysis,
    get_companies,
    get_sectors,
    get_market_cap_latest,
)

def load_data():

    ratios = get_latest_ratios()

    analysis = get_analysis()

    companies = get_companies()

    sectors = get_sectors()

    market = get_market_cap_latest()

    print("Ratios:", len(ratios), ratios["company_id"].nunique())
    print("Analysis:", len(analysis), analysis["company_id"].nunique())
    print("Companies:", len(companies), companies["id"].nunique())
    print("Sectors:", len(sectors), sectors["company_id"].nunique())
    print("Market:", len(market), market["company_id"].nunique())

    companies = companies.rename(
        columns={"id": "company_id"}
    )

    sectors = sectors.drop(
        columns=["id"],
        errors="ignore",
    )

    market = market.drop(
        columns=["id"],
        errors="ignore",
    )

    df = (
        ratios
        .merge(
            analysis,
            on="company_id",
            how="left",
        )
        .merge(
            companies,
            on="company_id",
            how="left",
        )
        .merge(
            sectors,
            on="company_id",
            how="left",
        )
        .merge(
            market,
            on="company_id",
            how="left",
        )
    )

    numeric_cols = [
        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "interest_coverage",
        "compounded_sales_growth",
        "compounded_profit_growth",
        "free_cash_flow_cr",
        "debt_to_equity",
        "pe_ratio",
        "pb_ratio",
        "dividend_yield_pct",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce",
            )

    df["composite_score"] = (
        df["return_on_equity_pct"].fillna(0) * 0.25
        + df["operating_profit_margin_pct"].fillna(0) * 0.20
        + df["interest_coverage"].fillna(0) * 0.15
        + df["compounded_sales_growth"].fillna(0) * 0.20
        + df["compounded_profit_growth"].fillna(0) * 0.20
    )

    print("Rows:", len(df))
    print("Unique companies:", df["company_id"].nunique())

    return df
def preset_filters():

    st.sidebar.subheader("⭐ Presets")

    preset = st.sidebar.radio(
        "Choose a Preset",
        [
            "Custom",
            "Quality",
            "Value",
            "Growth",
            "Dividend",
            "Debt-Free",
            "Turnaround",
        ],
    )

    return preset
def sidebar_filters(df):

    preset = preset_filters()

    st.sidebar.divider()
    st.sidebar.header("📊 Stock Screener")

    fcf_min = float(df["free_cash_flow_cr"].fillna(0).min())
    fcf_max = float(df["free_cash_flow_cr"].fillna(0).max())

    if fcf_min >= fcf_max:
        fcf_max = fcf_min + 1

    filters = {}

    filters["roe"] = st.sidebar.slider(
        "ROE % (Minimum)",
        0.0,
        50.0,
        0.0,
    )

    filters["de"] = st.sidebar.slider(
        "Debt / Equity (Maximum)",
        0.0,
        5.0,
        5.0,
    )

    filters["fcf"] = st.sidebar.slider(
        "Free Cash Flow (Minimum)",
        fcf_min,
        fcf_max,
        fcf_min,
    )

    filters["sales"] = st.sidebar.slider(
        "Revenue CAGR % (Minimum)",
        -50.0,
        100.0,
        -50.0,
    )

    filters["profit"] = st.sidebar.slider(
        "PAT CAGR % (Minimum)",
        -50.0,
        100.0,
        -50.0,
    )

    filters["opm"] = st.sidebar.slider(
        "Operating Margin % (Minimum)",
        0.0,
        70.0,
        0.0,
    )

    filters["pe"] = st.sidebar.slider(
        "P/E Ratio (Maximum)",
        0.0,
        150.0,
        150.0,
    )

    filters["pb"] = st.sidebar.slider(
        "P/B Ratio (Maximum)",
        0.0,
        30.0,
        30.0,
    )

    filters["dividend"] = st.sidebar.slider(
        "Dividend Yield % (Minimum)",
        0.0,
        10.0,
        0.0,
    )

    filters["icr"] = st.sidebar.slider(
        "Interest Coverage (Minimum)",
        0.0,
        100.0,
        0.0,
    )

    return filters
def apply_filters(df, filters):

    filtered = df.copy()

    filtered["return_on_equity_pct"] = filtered["return_on_equity_pct"].fillna(0)
    filtered["debt_to_equity"] = filtered["debt_to_equity"].fillna(999)
    filtered["free_cash_flow_cr"] = filtered["free_cash_flow_cr"].fillna(0)
    filtered["compounded_sales_growth"] = filtered["compounded_sales_growth"].fillna(-50)
    filtered["compounded_profit_growth"] = filtered["compounded_profit_growth"].fillna(-50)
    filtered["operating_profit_margin_pct"] = filtered["operating_profit_margin_pct"].fillna(0)
    filtered["pe_ratio"] = filtered["pe_ratio"].fillna(999)
    filtered["pb_ratio"] = filtered["pb_ratio"].fillna(999)
    filtered["dividend_yield_pct"] = filtered["dividend_yield_pct"].fillna(0)
    filtered["interest_coverage"] = filtered["interest_coverage"].fillna(0)

    print("Start:", len(filtered))

    filtered = filtered[
        filtered["return_on_equity_pct"] >= filters["roe"]
    ]
    print("After ROE:", len(filtered))

    filtered = filtered[
        filtered["debt_to_equity"] <= filters["de"]
    ]
    print("After Debt/Equity:", len(filtered))

    filtered = filtered[
        filtered["free_cash_flow_cr"] >= filters["fcf"]
    ]
    print("After FCF:", len(filtered))

    filtered = filtered[
        filtered["compounded_sales_growth"] >= filters["sales"]
    ]
    print("After Revenue CAGR:", len(filtered))

    filtered = filtered[
        filtered["compounded_profit_growth"] >= filters["profit"]
    ]
    print("After PAT CAGR:", len(filtered))

    filtered = filtered[
        filtered["operating_profit_margin_pct"] >= filters["opm"]
    ]
    print("After OPM:", len(filtered))

    filtered = filtered[
        filtered["pe_ratio"] <= filters["pe"]
    ]
    print("After PE:", len(filtered))

    filtered = filtered[
        filtered["pb_ratio"] <= filters["pb"]
    ]
    print("After PB:", len(filtered))

    filtered = filtered[
        filtered["dividend_yield_pct"] >= filters["dividend"]
    ]
    print("After Dividend:", len(filtered))

    filtered = filtered[
        filtered["interest_coverage"] >= filters["icr"]
    ]
    print("After Interest Coverage:", len(filtered))

    return filtered
def render_table(df):

    st.subheader("📊 Filtered Companies")

    st.info(f"📌 {len(df)} companies match your filters.")

    df = df.sort_values(
        "composite_score",
        ascending=False,
    )

    cols = [
        "company_id",
        "company_name",
        "broad_sector",
        "composite_score",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "compounded_sales_growth",
        "compounded_profit_growth",
        "operating_profit_margin_pct",
        "pe_ratio",
        "pb_ratio",
        "dividend_yield_pct",
        "interest_coverage",
    ]

    st.dataframe(
        df[cols],
        width="stretch",
        hide_index=True,
    )
def csv_download(df):

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="screener_results.csv",
        mime="text/csv",
    )
def show():

    st.title("🔎 Stock Screener")

    df = load_data()

    filters = sidebar_filters(df)

    filtered = apply_filters(df, filters)

    render_table(filtered)

    st.divider()

    csv_download(filtered)