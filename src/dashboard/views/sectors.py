import pandas as pd
import plotly.express as px
import streamlit as st
from utils.db import (
    get_analysis,
    get_companies,
    get_latest_ratios,
    get_market_cap_latest,
    get_sectors,
)


def load_data():
    """Load and merge ratios, analysis, company metadata, sectors, and market cap metrics."""

    ratios = get_latest_ratios()
    analysis = get_analysis()
    companies = get_companies()
    sectors = get_sectors()
    market = get_market_cap_latest()

    ratios = ratios.drop(columns=["id"], errors="ignore")
    sectors = sectors.drop(columns=["id"], errors="ignore")
    market = market.drop(columns=["id"], errors="ignore")

    df = (
        ratios.merge(
            analysis,
            on="company_id",
            how="left",
        )
        .merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left",
            suffixes=("", "_company"),
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
            suffixes=("", "_market"),
        )
    )

    return df


def sector_selector(df):
    """Render a select box for choosing a broad sector from the dataframe."""

    sectors = sorted(df["broad_sector"].dropna().unique())

    return st.selectbox(
        "Select Sector",
        sectors,
    )


def bubble_chart(df, sector):
    """Generate and display a bubble chart comparing FCF, ROE, and market cap for a sector."""

    sector_df = df[df["broad_sector"] == sector].copy()

    sector_df["free_cash_flow_cr"] = pd.to_numeric(
        sector_df["free_cash_flow_cr"],
        errors="coerce",
    )

    sector_df["return_on_equity_pct"] = pd.to_numeric(
        sector_df["return_on_equity_pct"],
        errors="coerce",
    )

    sector_df["market_cap_crore"] = pd.to_numeric(
        sector_df["market_cap_crore"],
        errors="coerce",
    )

    sector_df = sector_df.dropna(
        subset=[
            "free_cash_flow_cr",
            "return_on_equity_pct",
            "market_cap_crore",
        ]
    )

    sector_df = sector_df[sector_df["market_cap_crore"] > 0]

    if sector_df.empty:

        st.warning("No valid data available for this sector.")
        return

    fig = px.scatter(
        sector_df,
        x="free_cash_flow_cr",
        y="return_on_equity_pct",
        size="market_cap_crore",
        color="sub_sector",
        hover_name="company_name",
        hover_data={
            "market_cap_crore": ":,.0f",
            "free_cash_flow_cr": ":,.2f",
            "return_on_equity_pct": ":.2f",
        },
        labels={
            "free_cash_flow_cr": "Free Cash Flow (Cr)",
            "return_on_equity_pct": "ROE (%)",
        },
        title=f"{sector} Companies",
        size_max=50,
    )

    fig.update_traces(
        marker={
            "opacity": 0.8,
            "line": {"width": 1, "color": "black"},
        }
    )

    fig.update_layout(
        template="plotly_white",
        height=650,
        xaxis_title="Free Cash Flow (Cr)",
        yaxis_title="ROE (%)",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


def show():
    """Display the Sector Analysis Streamlit dashboard page."""

    st.title("🏭 Sector Analysis")

    df = load_data()

    sector = sector_selector(df)

    bubble_chart(
        df,
        sector,
    )
