from fastapi import APIRouter, HTTPException
import pandas as pd
from fastapi.responses import FileResponse
from pathlib import Path
from src.dashboard.utils.db import (
    get_companies,
    get_latest_ratios,
    get_company,
    get_company_ratios,
    get_company_sector,
    get_profit_loss,
    get_balance_sheet,
    get_cashflow,
    get_documents,
    get_sectors,
)

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

import math


def clean_df(df: pd.DataFrame):
    if df is None or df.empty:
        return df

    df = df.astype(object)

    df = df.where(pd.notna(df), None)

    return df.replace({float("nan"): None})


def build_company_dataframe():

    companies = clean_df(get_companies().copy())
    sectors = clean_df(get_sectors().copy())
    latest = clean_df(get_latest_ratios().copy())

    sectors.drop(
        columns=["id"],
        errors="ignore",
        inplace=True,
    )

    latest.drop(
        columns=["id"],
        errors="ignore",
        inplace=True,
    )

    df = companies.merge(
        sectors,
        left_on="id",
        right_on="company_id",
        how="left",
    )

    df = df.merge(
        latest,
        left_on="id",
        right_on="company_id",
        how="left",
        suffixes=("", "_ratio"),
    )

    df.drop(
        columns=[
            "company_id",
            "company_id_ratio",
        ],
        errors="ignore",
        inplace=True,
    )

    return clean_df(df)
# ---------------------------------------------------------
# GET ALL COMPANIES
# ---------------------------------------------------------

@router.get("/")
def list_companies():

    df = build_company_dataframe()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No companies found",
        )

    return clean_df(df).to_dict(orient="records")


# ---------------------------------------------------------
# GET COMPANY
# ---------------------------------------------------------

@router.get("/{ticker}")
def company_profile(ticker: str):

    company = clean_df(get_company(ticker))

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    sector = clean_df(get_company_sector(ticker))
    ratios = clean_df(get_company_ratios(ticker))

    response = company.iloc[0].to_dict()

    if not sector.empty:
        response["sector"] = sector.iloc[0].to_dict()

    if not ratios.empty:
        latest_ratio = (
            ratios.sort_values("year")
            .iloc[-1]
            .to_dict()
        )

        response["latest_ratio"] = latest_ratio

    return response
# ---------------------------------------------------------
# PROFIT & LOSS
# ---------------------------------------------------------

@router.get("/{ticker}/pl")
def company_profit_loss(
    ticker: str,
    year: int | None = None,
):

    df = clean_df(get_profit_loss(ticker))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Profit & Loss data not found",
        )

    if year is not None:
        df = df[df["year"] == year]

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for {year}",
            )

    return clean_df(df).to_dict(orient="records")


# ---------------------------------------------------------
# BALANCE SHEET
# ---------------------------------------------------------

@router.get("/{ticker}/bs")
def company_balance_sheet(
    ticker: str,
    year: int | None = None,
):

    df = clean_df(get_balance_sheet(ticker))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Balance Sheet data not found",
        )

    if year is not None:
        df = df[df["year"] == year]

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for {year}",
            )

    return clean_df(df).to_dict(orient="records")


# ---------------------------------------------------------
# CASH FLOW
# ---------------------------------------------------------

@router.get("/{ticker}/cashflow")
def company_cashflow(
    ticker: str,
    year: int | None = None,
):

    df = clean_df(get_cashflow(ticker))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Cash Flow data not found",
        )

    if year is not None:
        df = df[df["year"] == year]

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for {year}",
            )

    return clean_df(df).to_dict(orient="records")


# ---------------------------------------------------------
# FINANCIAL RATIOS
# ---------------------------------------------------------

@router.get("/{ticker}/ratios")
def company_ratios(
    ticker: str,
    year: int | None = None,
):

    df = clean_df(get_company_ratios(ticker))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Financial Ratios not found",
        )

    if year is not None:
        df = df[df["year"] == year]

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for {year}",
            )

    return clean_df(df).to_dict(orient="records")
# ---------------------------------------------------------
# DOCUMENTS
# ---------------------------------------------------------

@router.get("/{ticker}/documents")
def company_documents(ticker: str):

    company = get_company(ticker)

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    df = clean_df(get_documents(ticker))

    if df.empty:
        return {
            "company_id": ticker,
            "documents": [],
            "count": 0,
        }

    return {
        "company_id": ticker,
        "count": len(df),
        "documents": df.to_dict(orient="records"),
    }


# ---------------------------------------------------------
# COMPANY TEARSHEET
# ---------------------------------------------------------

@router.get("/{ticker}/tearsheet")
@router.get("/{ticker}/tearsheet")
def company_tearsheet(ticker: str):

    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    pdf_path = (
        PROJECT_ROOT
        / "reports"
        / "tearsheets"
        / f"{ticker.upper()}_tearsheet.pdf"
    )

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Tearsheet not found for {ticker}",
        )

    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=f"{ticker.upper()}_tearsheet.pdf",
    )

# ---------------------------------------------------------
# PING
# ---------------------------------------------------------

@router.get("/ping")
def ping():

    return {
        "status": "ok",
        "service": "companies",
    }