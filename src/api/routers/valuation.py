import pandas as pd
from fastapi import APIRouter, HTTPException

from src.dashboard.utils.db import (
    get_market_cap,
    get_market_cap_latest,
)

router = APIRouter(
    prefix="/valuation",
    tags=["Valuation"],
)


def clean_df(df):
    """Replace NaN values with None in a DataFrame for JSON serialization."""

    if df is None or df.empty:
        return df

    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    return df


@router.get("/")
def latest_valuations():
    """Retrieve the latest market cap and valuation metrics for all companies."""

    df = clean_df(get_market_cap_latest())

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Valuation data not found",
        )

    return {
        "count": len(df),
        "valuations": df.to_dict(orient="records"),
    }


@router.get("/{ticker}")
def company_valuation(ticker: str):
    """Retrieve historical market capitalization and valuation data for a specific company."""

    df = clean_df(get_market_cap())

    df = df[df["company_id"].astype(str).str.upper() == ticker.upper()]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{ticker} not found",
        )

    return {
        "company": ticker.upper(),
        "history": df.to_dict(orient="records"),
    }


@router.get("/{ticker}/latest")
def latest_company_valuation(ticker: str):
    """Retrieve the single most recent valuation record for a specific company."""

    df = clean_df(get_market_cap_latest())

    df = df[df["company_id"].astype(str).str.upper() == ticker.upper()]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{ticker} not found",
        )

    return df.to_dict(orient="records")[0]
