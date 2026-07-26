import pandas as pd
import plotly.express as px
import streamlit as st
from utils.db import (
    get_all_company_ids,
    get_balance_sheet,
    get_cashflow,
    get_company_cashflow_intelligence,
    get_profit_loss,
)


def company_selector():
    """Display a dropdown select box for choosing a company ticker."""
    companies = get_all_company_ids()
    return st.selectbox("Select Company", companies)


def plot_table(df, title):
    """Display a formatted dataframe table in Streamlit with a subheader."""

    st.subheader(title)

    if df.empty:
        st.warning("No data available.")
        return

    st.dataframe(df, use_container_width=True)


def plot_chart(df, title):
    """Render an interactive Plotly line chart for a selected dataframe metric."""

    if df.empty:
        return

    value_columns = [c for c in df.columns if c not in ["id", "company_id", "year"]]

    if not value_columns:
        return

    metric = st.selectbox(
        f"{title} Metric",
        value_columns,
        key=title,
    )

    chart_df = df.copy()

    chart_df[metric] = pd.to_numeric(
        chart_df[metric],
        errors="coerce",
    )

    chart_df["year"] = chart_df["year"].astype(str)

    fig = px.line(
        chart_df,
        x="year",
        y=metric,
        markers=True,
        title=f"{metric} Trend",
    )

    fig.update_layout(
        template="plotly_white",
        height=450,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


def show():
    """Display the Capital Allocation Streamlit dashboard page."""

    st.title("💰 Capital Allocation")

    company = company_selector()

    pl = get_profit_loss(company)
    cf = get_cashflow(company)
    bs = get_balance_sheet(company)
    intel = get_company_cashflow_intelligence(company)

    if not intel.empty:

        row = intel.iloc[0]

        st.subheader("📊 Cash Flow Intelligence")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "CFO Quality Score",
            f"{row['cfo_quality_score']:.2f}",
        )

        c2.metric(
            "Quality",
            row["cfo_quality_label"],
        )

        c3.metric(
            "FCF Conversion",
            f"{row['fcf_conversion_pct']:.1f}%",
        )

        c4.metric(
            "5Y FCF CAGR",
            f"{row['fcf_cagr_5y_pct']:.1f}%",
        )

        c5, c6 = st.columns(2)

        c5.metric(
            "Distress",
            "🚨 Yes" if row["distress_flag"] else "✅ No",
        )

        c6.metric(
            "Deleveraging",
            "✅ Yes" if row["deleveraging_flag"] else "❌ No",
        )

        if "capital_allocation_label" in intel.columns and pd.notna(
            row["capital_allocation_label"]
        ):
            st.success(
                f"Capital Allocation Pattern: **{row['capital_allocation_label']}**"
            )

        st.divider()

    else:
        st.info("Cash Flow Intelligence data not available.")

    tab1, tab2, tab3 = st.tabs(
        [
            "📈 Profit & Loss",
            "💵 Cash Flow",
            "🏦 Balance Sheet",
        ]
    )

    with tab1:

        plot_table(pl, "Profit & Loss")
        plot_chart(pl, "Profit & Loss")

    with tab2:

        plot_table(cf, "Cash Flow")
        plot_chart(cf, "Cash Flow")

        if not cf.empty and "net_cash_flow" in cf.columns:

            chart_df = cf.copy()

            chart_df["net_cash_flow"] = pd.to_numeric(
                chart_df["net_cash_flow"],
                errors="coerce",
            )

            chart_df["year"] = chart_df["year"].astype(str)

            fig = px.bar(
                chart_df,
                x="year",
                y="net_cash_flow",
                color="net_cash_flow",
                title="Net Cash Flow",
            )

            fig.update_layout(
                template="plotly_white",
                height=450,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    with tab3:

        plot_table(bs, "Balance Sheet")
        plot_chart(bs, "Balance Sheet")
