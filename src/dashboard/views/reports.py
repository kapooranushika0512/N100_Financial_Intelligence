import streamlit as st
import pandas as pd

from utils.db import (
    get_all_company_ids,
    get_documents,
)


def company_selector():

    companies = get_all_company_ids()

    return st.selectbox(
        "Select Company",
        companies,
    )


def show_reports(df):

    st.subheader("Annual Reports")

    if df.empty:

        st.warning("No reports available.")

        return

    display = df.copy()

    if "url" in display.columns:

        def make_link(url):

            if pd.isna(url) or url == "":

                return "🔴 Report Unavailable"

            return f"[Open Report]({url})"

        display["Report"] = display["url"].apply(make_link)

    st.dataframe(
        display,
        width="stretch",
        hide_index=True,
    )


def show():

    st.title("📄 Annual Reports")

    company = company_selector()

    reports = get_documents(company)

    show_reports(reports)