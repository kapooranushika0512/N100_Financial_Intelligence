import pandas as pd
import requests
from fastapi import APIRouter, HTTPException

from src.dashboard.utils.db import (
    get_all_company_ids,
    get_documents,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


def clean_df(df):
    """Replace NaN values with None in a DataFrame for JSON serialization."""

    if df is None or df.empty:
        return df

    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    return df


def check_url(url):
    """Validate whether a given URL is reachable via a HEAD request."""

    if not isinstance(url, str):
        return False

    if not url.startswith("http"):
        return False

    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=5,
        )
        return response.status_code < 400

    except requests.RequestException:
        return False


@router.get("/")
def all_documents():
    """Retrieve document counts for all tracked companies."""

    companies = get_all_company_ids()

    result = []

    for company in companies:
        df = clean_df(get_documents(company))

        result.append(
            {
                "company_id": company,
                "documents": len(df),
            }
        )

    return {
        "companies": len(result),
        "results": result,
    }


@router.get("/{ticker}")
def company_documents(ticker: str):
    """Retrieve documents and validate URL accessibility for a specific company."""

    df = clean_df(get_documents(ticker))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{ticker} not found",
        )

    if "url" in df.columns:
        df["is_url_valid"] = df["url"].apply(check_url)

    return {
        "company": ticker.upper(),
        "documents": df.to_dict(orient="records"),
    }
