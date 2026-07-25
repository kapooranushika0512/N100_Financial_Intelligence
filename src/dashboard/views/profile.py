import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.db import (
    get_all_company_ids,
    get_company,
    get_company_ratios,
    get_company_sector,
    get_company_pros_cons,
    get_profit_loss,
)
def render_company_header(company, sector, company_id):

    left, right = st.columns([1, 4])

    with left:

        logo = company["company_logo"]

        # Temporary: show the logo URL for debugging
        st.write("Logo URL:", logo)

        if (
            pd.notna(logo)
            and isinstance(logo, str)
            and logo.startswith("http")
        ):
            try:
                st.image(logo, width=120)
            except Exception as e:
                st.error(e)
                st.markdown("# 🏢")
        else:
            st.markdown("# 🏢")

    with right:

        st.markdown(f"## {company['company_name']}")

        st.caption(company_id)

        if not sector.empty:
            sector = sector.iloc[0]

            st.write(
                f"**Sector:** {sector['broad_sector']}"
            )

            st.write(
                f"**Sub Sector:** {sector['sub_sector']}"
            )

        st.write(company["about_company"])

        website = company["website"]

        if (
            pd.notna(website)
            and isinstance(website, str)
            and website.startswith("http")
        ):
            st.link_button(
                "🌐 Visit Company Website",
                website,
            )

    st.divider()
def render_kpi_cards(ratios):

    st.divider()

    st.subheader("📊 Financial Snapshot")

    if ratios.empty:
        st.info("Financial ratios not available.")
        return

    latest = ratios.iloc[-1]

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "ROE %",
            round(latest["return_on_equity_pct"], 2)
        )

        st.metric(
            "Net Profit Margin %",
            round(latest["net_profit_margin_pct"], 2)
        )

    with c2:

        st.metric(
            "Operating Margin %",
            round(latest["operating_profit_margin_pct"], 2)
        )

        st.metric(
            "Debt / Equity",
            round(latest["debt_to_equity"], 2)
        )

    with c3:

        st.metric(
            "Interest Coverage",
            round(latest["interest_coverage"], 2)
        )

        st.metric(
            "Free Cash Flow (₹ Cr)",
            round(latest["free_cash_flow_cr"], 2)
        )
def render_revenue_profit_chart(pl):

    st.divider()

    st.subheader("📈 Revenue vs Net Profit (10 Years)")

    if pl.empty:
        st.info("Profit & Loss data not available.")
        return

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=pl["year"],
            y=pl["sales"],
            name="Revenue",
        )
    )

    fig.add_trace(
        go.Bar(
            x=pl["year"],
            y=pl["net_profit"],
            name="Net Profit",
        )
    )

    fig.update_layout(
        barmode="group",
        height=450,
        title="Revenue & Net Profit Trend",
        xaxis_title="Financial Year",
        yaxis_title="₹ Crore",
        legend_title="Metrics",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )
def render_roe_roce_chart(ratios, company):

    st.divider()

    st.subheader("📉 ROE & ROCE Trend")

    if ratios.empty:
        st.info("ROE history not available.")
        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ratios["year"],
            y=ratios["return_on_equity_pct"],
            mode="lines+markers",
            name="ROE %",
            line=dict(width=3),
        )
    )

    roce = company["roce_percentage"]

    fig.add_trace(
        go.Scatter(
            x=ratios["year"],
            y=[roce] * len(ratios),
            mode="lines",
            name="Current ROCE %",
            line=dict(
                dash="dash",
                width=3,
            ),
        )
    )

    fig.update_layout(
        height=450,
        title="Return on Equity vs ROCE",
        xaxis_title="Financial Year",
        yaxis_title="Percentage (%)",
        hovermode="x unified",
        legend_title="Metrics",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )
def render_pros_cons(pros_cons):

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("✅ Pros")

        if pros_cons.empty:
            st.info("No pros available.")
        else:

            pros = str(pros_cons.iloc[0]["pros"])

            if pros.strip():

                for item in pros.split(";"):

                    item = item.strip()

                    if item:
                        st.success(item)

            else:
                st.info("No pros available.")

    with right:

        st.subheader("❌ Cons")

        if pros_cons.empty:
            st.info("No cons available.")
        else:

            cons = str(pros_cons.iloc[0]["cons"])

            if cons.strip():

                for item in cons.split(";"):

                    item = item.strip()

                    if item:
                        st.error(item)

            else:
                st.info("No cons available.")
def render_ratio_table(ratios):

    st.divider()

    st.subheader("📊 Financial Ratios")

    if ratios.empty:
        st.info("Financial ratios not available.")
        return

    display = ratios[
        [
            "year",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
        ]
    ].copy()

    display.columns = [
        "Year",
        "ROE %",
        "Net Margin %",
        "Operating Margin %",
        "Debt / Equity",
        "Interest Coverage",
        "Asset Turnover",
        "Free Cash Flow (₹ Cr)",
    ]

    st.dataframe(
        display,
        width="stretch",
        hide_index=True,
    )
def render_profit_loss_table(pl):

    st.divider()

    st.subheader("📑 Profit & Loss Statement")

    if pl.empty:
        st.info("Profit & Loss data not available.")
        return

    display = pl[
        [
            "year",
            "sales",
            "expenses",
            "operating_profit",
            "profit_before_tax",
            "net_profit",
            "eps",
        ]
    ].copy()

    display.columns = [
        "Year",
        "Revenue (₹ Cr)",
        "Expenses (₹ Cr)",
        "Operating Profit (₹ Cr)",
        "Profit Before Tax (₹ Cr)",
        "Net Profit (₹ Cr)",
        "EPS",
    ]

    st.dataframe(
        display,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        f"Showing {len(display)} financial years."
    )
def show():

    st.title("🏢 Company Profile")

    company_ids = get_all_company_ids()

    company_id = st.selectbox(
        "🔍 Search Company",
        company_ids,
        index=0,
        help="Select a company ticker",
    )

    company_df = get_company(company_id)

    if company_df.empty:
        st.warning("Ticker not found — please try another.")
        return

    company = company_df.iloc[0]

    sector = get_company_sector(company_id)

    ratios = get_company_ratios(company_id)

    pl = get_profit_loss(company_id)

    pros_cons = get_company_pros_cons(company_id)

    render_company_header(
        company,
        sector,
        company_id,
    )

    render_kpi_cards(
        ratios,
    )

    render_revenue_profit_chart(
        pl,
    )

    render_roe_roce_chart(
        ratios,
        company,
    )

    render_pros_cons(
        pros_cons,
    )

    render_ratio_table(
        ratios,
    )

    render_profit_loss_table(
        pl,
    )