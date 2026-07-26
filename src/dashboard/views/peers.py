import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.db import (
    get_latest_ratio,
    get_peer_companies,
    get_peer_groups,
)


def load_data():
    """Load peer groups dataset from the database."""

    peer_groups = get_peer_groups()

    return peer_groups


def peer_selector(peer_groups):
    """Render a select box for picking a peer group."""

    groups = sorted(peer_groups["peer_group_name"].unique())

    selected_group = st.selectbox(
        "Select Peer Group",
        groups,
    )

    return selected_group


def company_selector(selected_group):
    """Render a select box for picking a company within a peer group."""

    companies = get_peer_companies(selected_group)

    company = st.selectbox(
        "Select Company",
        companies["company_name"],
    )

    return company, companies


def create_radar_chart(selected_group, company):
    """Generate and display a polar radar chart comparing a company to its peer average."""

    company_id = (
        get_peer_companies(selected_group)
        .loc[
            lambda x: x["company_name"] == company,
            "company_id",
        ]
        .iloc[0]
    )

    company_ratio = get_latest_ratio(company_id)

    if company_ratio.empty:
        st.warning("No financial ratios available.")
        return

    company_ratio = company_ratio.iloc[0]

    peer_companies = get_peer_companies(selected_group)

    metrics = [
        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "earnings_per_share",
        "book_value_per_share",
        "debt_to_equity",
    ]

    peer_avg = {}

    for metric in metrics:
        values = []

        for cid in peer_companies["company_id"]:
            r = get_latest_ratio(cid)

            if not r.empty:
                value = r.iloc[0][metric]

                if pd.notna(value):
                    values.append(value)

        peer_avg[metric] = sum(values) / len(values) if values else 0

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=[company_ratio[m] for m in metrics],
            theta=metrics,
            fill="toself",
            name=company,
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[peer_avg[m] for m in metrics],
            theta=metrics,
            fill="toself",
            name="Peer Average",
        )
    )

    fig.update_layout(
        polar={
            "radialaxis": {
                "visible": True,
            },
        },
        height=600,
    )

    st.subheader("📊 Radar Comparison")

    st.plotly_chart(
        fig,
        width="stretch",
    )


def peer_table(selected_group):
    """Render a table comparing KPIs across all companies in a peer group."""

    peers = get_peer_companies(selected_group)

    rows = []

    for _, row in peers.iterrows():
        ratio = get_latest_ratio(row["company_id"])

        if ratio.empty:
            continue

        ratio = ratio.iloc[0]

        rows.append(
            {
                "Company": row["company_name"],
                "Benchmark": "⭐" if row["is_benchmark"] else "",
                "ROE": ratio["return_on_equity_pct"],
                "OPM": ratio["operating_profit_margin_pct"],
                "Debt/Equity": ratio["debt_to_equity"],
                "Interest Coverage": ratio["interest_coverage"],
                "EPS": ratio["earnings_per_share"],
                "Book Value": ratio["book_value_per_share"],
                "FCF": ratio["free_cash_flow_cr"],
            }
        )

    table = pd.DataFrame(rows)

    st.subheader("📋 Peer KPI Comparison")

    def highlight(row):
        if row["Benchmark"] == "⭐":
            return ["background-color:#FFF3B0"] * len(row)
        return [""] * len(row)

    st.dataframe(
        table.style.apply(
            highlight,
            axis=1,
        ),
        width="stretch",
    )


def show():
    """Display the Peer Comparison Streamlit page."""

    st.title("👥 Peer Comparison")

    peer_groups = load_data()

    selected_group = peer_selector(peer_groups)

    company, _ = company_selector(selected_group)

    st.write(f"### Selected Peer Group: {selected_group}")
    st.write(f"Selected Company: {company}")

    create_radar_chart(
        selected_group,
        company,
    )

    peer_table(selected_group)


if __name__ == "__main__":
    show()
