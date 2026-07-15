import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_all_company_ids,
    get_profit_loss,
    get_cashflow,
    get_balance_sheet,
)


def company_selector():

    companies = get_all_company_ids()

    return st.selectbox(
        "Select Company",
        companies,
    )


def plot_table(df, title):

    st.subheader(title)

    if df.empty:
        st.warning("No data available.")
        return

    st.dataframe(
        df,
        width="stretch",
    )


def plot_chart(df, title):

    if df.empty:
        return

    value_columns = [
        c for c in df.columns
        if c not in ["id", "company_id", "year"]
    ]

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

    fig = px.line(
        chart_df,
        x="year",
        y=metric,
        markers=True,
        title=f"{title} - {metric}",
    )

    fig.update_layout(
        template="plotly_white",
        height=450,
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


def show():

    st.title("💰 Capital Allocation")

    company = company_selector()

    pl = get_profit_loss(company)
    cf = get_cashflow(company)
    bs = get_balance_sheet(company)

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

    with tab3:
        plot_table(bs, "Balance Sheet")
        plot_chart(bs, "Balance Sheet")