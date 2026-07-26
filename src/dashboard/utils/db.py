import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def query(sql, params=None):
    """Execute an SQL query against the SQLite database and return a DataFrame."""

    conn = sqlite3.connect(str(DB_PATH))

    if params:
        df = pd.read_sql(sql, conn, params=params)
    else:
        df = pd.read_sql(sql, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_companies():
    """Retrieve all company records from the database."""

    return query("SELECT * FROM companies")


@st.cache_data(ttl=600)
def get_ratios():
    """Retrieve all financial ratio records from the database."""

    return query("SELECT * FROM financial_ratios")


@st.cache_data(ttl=600)
def get_sectors():
    """Retrieve all sector records from the database."""

    return query("SELECT * FROM sectors")


@st.cache_data(ttl=600)
def get_analysis():
    """Retrieve all analysis records from the database."""

    return query("SELECT * FROM analysis")


@st.cache_data(ttl=600)
def get_company(company_id):
    """Retrieve company details for a specific company ID."""

    return query(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_company_ratios(company_id):
    """Retrieve historical financial ratios for a specific company ID."""

    return query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_company_sector(company_id):
    """Retrieve sector mapping for a specific company ID."""

    return query(
        """
        SELECT *
        FROM sectors
        WHERE company_id=?
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_company_pros_cons(company_id):
    """Retrieve pros and cons analysis for a specific company ID."""

    return query(
        """
        SELECT *
        FROM prosandcons
        WHERE company_id=?
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_profit_loss(company_id):
    """Retrieve profit and loss statement records for a specific company ID."""

    return query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_cashflow(company_id):
    """Retrieve cash flow statement records for a specific company ID."""

    return query(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_balance_sheet(company_id):
    """Retrieve balance sheet records for a specific company ID."""

    return query(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_documents(company_id):
    """Retrieve available documents for a specific company ID."""

    return query(
        """
        SELECT *
        FROM documents
        WHERE company_id=?
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_all_company_ids():
    """Retrieve a sorted list of all unique company IDs."""

    df = query("""
        SELECT id
        FROM companies
        ORDER BY id
        """)

    return df["id"].tolist()


@st.cache_data(ttl=600)
def get_latest_ratios():
    """Retrieve the most recent financial ratios for all companies."""

    return query("""
        SELECT fr.*
        FROM financial_ratios fr
        INNER JOIN
        (
            SELECT
                company_id,
                MAX(year) AS latest_year
            FROM financial_ratios
            GROUP BY company_id
        ) latest
        ON fr.company_id = latest.company_id
        AND fr.year = latest.latest_year
        """)


@st.cache_data(ttl=600)
def get_latest_ratio(company_id):
    """Retrieve the single most recent financial ratio record for a company ID."""

    return query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 1
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_market_cap():
    """Retrieve all market capitalization records."""

    return query("""
        SELECT *
        FROM market_cap
        """)


@st.cache_data(ttl=600)
def get_market_cap_latest():
    """Retrieve the most recent market capitalization records for all companies."""

    return query("""
        SELECT mc.*
        FROM market_cap mc
        INNER JOIN
        (
            SELECT
                company_id,
                MAX(year) AS latest_year
            FROM market_cap
            GROUP BY company_id
        ) latest
        ON mc.company_id = latest.company_id
        AND mc.year = latest.latest_year
        """)


@st.cache_data(ttl=600)
def get_peer_groups():
    """Retrieve all peer group mappings."""

    return query("""
        SELECT *
        FROM peer_groups
        """)


@st.cache_data(ttl=600)
def get_peer_group(group):
    """Retrieve peer group records for a specific group name."""

    return query(
        """
        SELECT *
        FROM peer_groups
        WHERE peer_group_name=?
        """,
        [group],
    )


@st.cache_data(ttl=600)
def get_company_peer(company_id):
    """Retrieve peer group assignment for a specific company ID."""

    return query(
        """
        SELECT *
        FROM peer_groups
        WHERE company_id=?
        """,
        [company_id],
    )


@st.cache_data(ttl=600)
def get_peer_percentiles():
    """Retrieve all peer percentile calculations."""

    return query("""
        SELECT *
        FROM peer_percentiles
        """)


@st.cache_data(ttl=600)
def get_peer_companies(group):
    """Retrieve company names and benchmark flags for a specific peer group."""

    return query(
        """
        SELECT
            pg.company_id,
            c.company_name,
            pg.is_benchmark
        FROM peer_groups pg
        JOIN companies c
        ON pg.company_id = c.id
        WHERE pg.peer_group_name = ?
        ORDER BY c.company_name
        """,
        [group],
    )


@st.cache_data(ttl=600)
def get_cashflow_intelligence():
    """Load cash flow intelligence output metrics from an Excel file."""

    output = PROJECT_ROOT / "output" / "cashflow_intelligence.xlsx"

    if not output.exists():
        return pd.DataFrame()

    try:
        return pd.read_excel(output)
    except (ValueError, OSError, ImportError, RuntimeError):
        return pd.DataFrame()


@st.cache_data(ttl=600)
def get_company_cashflow_intelligence(company):
    """Retrieve cash flow intelligence metrics for a specific company ID."""

    df = get_cashflow_intelligence()

    if df.empty:
        return df

    return df[df.company_id == company]
