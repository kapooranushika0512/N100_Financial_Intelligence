import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.db import (
    get_all_company_ids,
    get_company_ratios,
)


def company_selector():
    """Render a dropdown select box for choosing a company ticker."""

    companies = get_all_company_ids()

    return st.selectbox(
        "Select Company",
        companies,
    )


def load_data(company):
    """Load and chronologically sort historical financial ratios for a company."""

    df = get_company_ratios(company)

    if not df.empty:
        df = df.sort_values("year")

    return df


def metric_selector(df):
    """Render a multiselect box allowing choice of up to three ratio metrics."""

    metrics = [
        col
        for col in df.columns
        if col
        not in [
            "id",
            "company_id",
            "year",
        ]
    ]

    return st.multiselect(
        "Select up to 3 Metrics",
        metrics,
        default=metrics[:1],
        max_selections=3,
    )


def trend_chart(df, metrics):
    """Generate and display an interactive Plotly line chart with YoY percentage calculations."""

    fig = go.Figure()

    for metric in metrics:

        values = pd.to_numeric(
            df[metric],
            errors="coerce",
        )

        yoy = values.pct_change() * 100

        hover = []

        for value, change in zip(values, yoy, strict=False):

            if pd.isna(change):
                hover.append(f"Value: {value:.2f}<br>YoY: N/A")
            else:
                hover.append(f"Value: {value:.2f}<br>YoY: {change:+.1f}%")

        fig.add_trace(
            go.Scatter(
                x=df["year"],
                y=values,
                mode="lines+markers",
                name=metric,
                line={"width": 3},
                marker={"size": 8},
                text=hover,
                hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
            )
        )

    fig.update_layout(
        title="10-Year Trend Analysis",
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title="Value",
        hovermode="x unified",
        height=600,
        margin={"l": 40, "r": 40, "t": 60, "b": 40},
        legend={
            "orientation": "h",
            "y": 1.08,
            "x": 0,
        },
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


def show():
    """Display the Trend Analysis Streamlit dashboard page."""

    st.title("📈 Trend Analysis")

    company = company_selector()

    df = load_data(company)

    if df.empty:

        st.warning("No financial data available.")

        return

    metrics = metric_selector(df)

    if len(metrics) == 0:

        st.info("Select at least one metric.")

        return

    trend_chart(
        df,
        metrics,
    )
