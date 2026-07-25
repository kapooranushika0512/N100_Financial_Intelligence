from fastapi import APIRouter, HTTPException
import pandas as pd

from src.dashboard.utils.db import get_market_cap

router = APIRouter(
    prefix="/market-cap",
    tags=["Market Cap"],
)


def clean_df(df):

    if df is None or df.empty:
        return df

    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    return df


@router.get("/{ticker}")
def market_cap_history(ticker: str):

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