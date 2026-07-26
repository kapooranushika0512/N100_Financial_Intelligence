import plotly.express as px
import streamlit as st
from utils.db import get_companies, get_ratios, get_sectors


def show():
    """Display the Dashboard Overview Streamlit page."""

    st.title("🏠 Dashboard Overview")

    ratios = get_ratios()
    companies = get_companies()
    sectors = get_sectors()

    ratios["year"] = ratios["year"].astype(str)

    years = sorted(ratios["year"].dropna().unique())

    selected_year = st.sidebar.selectbox("Select Year", years, index=len(years) - 1)

    ratios = ratios[ratios["year"] == selected_year]

    merged = ratios.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left",
        suffixes=("", "_company"),
    ).merge(sectors, on="company_id", how="left")

    st.subheader("📊 Key Performance Indicators")

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    c1.metric("Average ROE", f"{merged['return_on_equity_pct'].mean():.2f}%")

    c2.metric("Median Debt / Equity", f"{merged['debt_to_equity'].median():.2f}")

    c3.metric(
        "Average Net Profit Margin", f"{merged['net_profit_margin_pct'].mean():.2f}%"
    )

    c4.metric("Average Asset Turnover", f"{merged['asset_turnover'].mean():.2f}")

    c5.metric("Average Interest Coverage", f"{merged['interest_coverage'].mean():.2f}")

    debt_free = (merged["debt_to_equity"] <= 0).sum()

    c6.metric("Debt Free Companies", int(debt_free))

    st.divider()

    left, right = st.columns([1.4, 1])

    with left:

        st.subheader("🏭 Sector Distribution")

        sector_count = (
            merged.groupby("broad_sector").size().reset_index(name="Companies")
        )

        fig = px.pie(
            sector_count,
            names="broad_sector",
            values="Companies",
            hole=0.55,
            title="Companies by Sector",
        )

        fig.update_layout(height=500, legend_title="Sector")

        st.plotly_chart(
            fig,
            width="stretch",
        )

    with right:

        st.subheader("🏆 Top 5 Companies by ROE")

        top5 = (
            merged[
                [
                    "company_name",
                    "return_on_equity_pct",
                    "net_profit_margin_pct",
                    "debt_to_equity",
                ]
            ]
            .sort_values(by="return_on_equity_pct", ascending=False)
            .head(5)
        )

        st.dataframe(top5, width="stretch", hide_index=True)

    st.divider()

    st.subheader("📈 Data Summary")

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric("Rows Loaded", len(merged))

    summary2.metric("Unique Companies", merged["company_id"].nunique())

    summary3.metric("Available Sectors", merged["broad_sector"].nunique())

    st.info(
        "Use the sidebar to explore Company Profile, Screener, Peer Comparison, Trend Analysis, Sector Analysis, Capital Allocation and Annual Reports."
    )
