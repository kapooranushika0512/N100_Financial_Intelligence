import streamlit as st
import pandas as pd

from utils.db import (
    get_latest_ratios,
    get_market_cap_latest,
    get_sectors,
    get_companies,
)
def load_data():

    ratios = get_latest_ratios()
    market = get_market_cap_latest()
    sectors = get_sectors()
    companies = get_companies()

    ratios = ratios.drop(columns=["id"], errors="ignore")
    market = market.drop(columns=["id"], errors="ignore")
    sectors = sectors.drop(columns=["id"], errors="ignore")

    df = (
        ratios
        .merge(
            market,
            on="company_id",
            how="left",
            suffixes=("", "_market"),
        )
        .merge(
            sectors,
            on="company_id",
            how="left",
        )
        .merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left",
        )
    )

    df["free_cash_flow_cr"] = pd.to_numeric(
        df["free_cash_flow_cr"],
        errors="coerce",
    )

    df["market_cap_crore"] = pd.to_numeric(
        df["market_cap_crore"],
        errors="coerce",
    )

    df["pe_ratio"] = pd.to_numeric(
        df["pe_ratio"],
        errors="coerce",
    )

    df["fcf_yield_pct"] = (
        df["free_cash_flow_cr"]
        / df["market_cap_crore"]
    ) * 100

    return df
def company_selector(df):

    return st.selectbox(
        "Select Company",
        sorted(df["company_id"].unique()),
    )
def calculate_flag(company_row, df):

    sector = company_row["broad_sector"]

    sector_pe = (
        df[
            df["broad_sector"] == sector
        ]["pe_ratio"]
        .median()
    )

    pe = company_row["pe_ratio"]

    if pd.isna(pe) or pd.isna(sector_pe):
        return "Unknown", sector_pe

    if pe > sector_pe * 1.5:
        return "🔴 Caution", sector_pe

    elif pe < sector_pe * 0.7:
        return "🟢 Discount", sector_pe

    else:
        return "🟡 Fair", sector_pe
def valuation_dashboard(company_row, sector_pe, flag):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "P/E Ratio",
            f"{company_row['pe_ratio']:.2f}",
        )

    with c2:
        st.metric(
            "Sector Median P/E",
            f"{sector_pe:.2f}",
        )

    with c3:
        st.metric(
            "FCF Yield",
            f"{company_row['fcf_yield_pct']:.2f}%",
        )

    with c4:
        st.metric(
            "Valuation",
            flag,
        )

    st.divider()

    st.dataframe(
        company_row.to_frame().T,
        width="stretch",
    )
def show():

    st.title("💹 Valuation Dashboard")

    df = load_data()

    company = company_selector(df)

    row = df[
        df["company_id"] == company
    ].iloc[0]

    flag, sector_pe = calculate_flag(
        row,
        df,
    )

    valuation_dashboard(
        row,
        sector_pe,
        flag,
    )
    