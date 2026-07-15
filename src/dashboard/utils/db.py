import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

# ---------------------------------------------------
# DATABASE HELPER
# ---------------------------------------------------

def query(sql, params=None):

    conn = sqlite3.connect(str(DB_PATH))

    if params:
        df = pd.read_sql(sql, conn, params=params)
    else:
        df = pd.read_sql(sql, conn)

    conn.close()

    return df
# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():

    return query(
        "SELECT * FROM companies"
    )


@st.cache_data(ttl=600)
def get_ratios():

    return query(
        "SELECT * FROM financial_ratios"
    )


@st.cache_data(ttl=600)
def get_sectors():

    return query(
        "SELECT * FROM sectors"
    )


@st.cache_data(ttl=600)
def get_analysis():

    return query(
        "SELECT * FROM analysis"
    )
# ---------------------------------------------------
# COMPANY PROFILE
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_company(company_id):

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

    df = query(
        """
        SELECT id
        FROM companies
        ORDER BY id
        """
    )

    return df["id"].tolist()
# ---------------------------------------------------
# SCREENER
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_latest_ratios():

    return query(
        """
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
        """
    )


@st.cache_data(ttl=600)
def get_latest_ratio(company_id):

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

    return query(
        """
        SELECT *
        FROM market_cap
        """
    )


@st.cache_data(ttl=600)
def get_market_cap_latest():

    return query(
        """
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
        """
    )
# ---------------------------------------------------
# PEER COMPARISON
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_peer_groups():

    return query(
        """
        SELECT *
        FROM peer_groups
        """
    )


@st.cache_data(ttl=600)
def get_peer_group(group):

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

    return query(
        """
        SELECT *
        FROM peer_percentiles
        """
    )


@st.cache_data(ttl=600)
def get_peer_companies(group):

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
