from fastapi import APIRouter, HTTPException
import pandas as pd

from src.dashboard.utils.db import (
    get_market_cap,
    get_market_cap_latest,
    get_latest_ratio,
)

router = APIRouter(
    prefix="/valuation",
    tags=["Valuation"],
)


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def clean_df(df):

    if df is None or df.empty:
        return df

    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    return df
# ---------------------------------------------------------
# LATEST VALUATIONS
# ---------------------------------------------------------

@router.get("/")
def latest_valuations():

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
# ---------------------------------------------------------
# COMPANY VALUATION
# ---------------------------------------------------------

@router.get("/{ticker}")
def company_valuation(ticker: str):

    df = clean_df(get_market_cap())

    df = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{ticker} not found",
        )

    return {
        "company": ticker.upper(),
        "history": df.to_dict(orient="records"),
    }
# ---------------------------------------------------------
# LATEST VALUATION
# ---------------------------------------------------------

@router.get("/{ticker}/latest")
def latest_company_valuation(ticker: str):

    df = clean_df(get_market_cap_latest())

    df = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{ticker} not found",
        )

    return df.to_dict(orient="records")[0]