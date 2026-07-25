from fastapi import APIRouter, HTTPException
import pandas as pd
import requests

from src.dashboard.utils.db import (
    get_documents,
    get_all_company_ids,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
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


def check_url(url):

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

    except Exception:
        return False


# ---------------------------------------------------------
# ALL COMPANIES DOCUMENT STATUS
# ---------------------------------------------------------

@router.get("/")
def all_documents():

    companies = get_all_company_ids()

    result = []

    for company in companies:

        df = clean_df(get_documents(company))

        result.append({
            "company_id": company,
            "documents": len(df),
        })

    return {
        "companies": len(result),
        "results": result,
    }


# ---------------------------------------------------------
# COMPANY DOCUMENTS
# ---------------------------------------------------------

@router.get("/{ticker}")
def company_documents(ticker: str):

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