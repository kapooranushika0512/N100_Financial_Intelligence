import pandas as pd
from fastapi import APIRouter, HTTPException

from src.dashboard.utils.db import (
    get_companies,
    get_latest_ratios,
    get_market_cap_latest,
    get_sectors,
)

router = APIRouter(
    prefix="/screener",
    tags=["Screener"],
)


def clean_df(df: pd.DataFrame):
    """Replace NaN values with None in a DataFrame for JSON serialization."""

    if df is None or df.empty:
        return df

    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    return df


def build_screener():
    """Build and merge companies, ratios, sectors, and market cap data for screening."""

    companies = clean_df(get_companies())
    ratios = clean_df(get_latest_ratios())
    sectors = clean_df(get_sectors())
    market = clean_df(get_market_cap_latest())

    ratios.drop(columns=["id"], inplace=True, errors="ignore")
    sectors.drop(columns=["id"], inplace=True, errors="ignore")
    market.drop(columns=["id"], inplace=True, errors="ignore")

    df = companies.merge(
        ratios,
        left_on="id",
        right_on="company_id",
        how="left",
    )

    df = df.merge(
        sectors,
        left_on="id",
        right_on="company_id",
        how="left",
        suffixes=("", "_sector"),
    )

    df = df.merge(
        market,
        left_on="id",
        right_on="company_id",
        how="left",
        suffixes=("", "_market"),
    )

    df.drop(
        columns=[
            "company_id",
            "company_id_sector",
            "company_id_market",
        ],
        inplace=True,
        errors="ignore",
    )

    return clean_df(df)


@router.get("/")
def screener():
    """Retrieve complete stock screener data across all companies."""

    df = build_screener()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No screener data found",
        )

    return df.to_dict(orient="records")


@router.get("/{ticker}")
def screener_company(ticker: str):
    """Retrieve screener metrics for a specific company ticker."""

    df = build_screener()

    df = df[df["id"] == ticker]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{ticker} not found",
        )

    return df.iloc[0].to_dict()


@router.get("/filter/")
def screener_filter(
    sector: str | None = None,
    min_roe: float | None = None,
    max_debt: float | None = None,
    min_npm: float | None = None,
    market_cap_category: str | None = None,
):
    """Filter company screener records based on specified financial metrics."""

    df = build_screener()

    if sector:
        df = df[df["broad_sector"].astype(str).str.lower() == sector.lower()]

    if min_roe is not None and "return_on_equity_pct" in df.columns:
        df = df[df["return_on_equity_pct"].fillna(0) >= min_roe]

    if max_debt is not None and "debt_to_equity" in df.columns:
        df = df[df["debt_to_equity"].fillna(99999) <= max_debt]

    if min_npm is not None and "net_profit_margin_pct" in df.columns:
        df = df[df["net_profit_margin_pct"].fillna(-99999) >= min_npm]

    if market_cap_category and "market_cap_category" in df.columns:
        df = df[
            df["market_cap_category"].astype(str).str.lower()
            == market_cap_category.lower()
        ]

    df = clean_df(df)

    return {
        "count": len(df),
        "companies": df.to_dict(orient="records"),
    }


@router.get("/sectors/list")
def screener_sectors():
    """Retrieve a list of unique broad sectors available in the screener."""

    df = build_screener()

    if "broad_sector" not in df.columns:
        return []

    sectors = df["broad_sector"].dropna().sort_values().unique().tolist()

    return sectors


@router.get("/marketcap/list")
def market_caps():
    """Retrieve a list of unique market capitalization categories available in the screener."""

    df = build_screener()

    if "market_cap_category" not in df.columns:
        return []

    caps = df["market_cap_category"].dropna().sort_values().unique().tolist()

    return caps
