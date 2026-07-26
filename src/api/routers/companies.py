from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from src.dashboard.utils.db import (
    get_balance_sheet,
    get_cashflow,
    get_companies,
    get_company,
    get_company_ratios,
    get_company_sector,
    get_documents,
    get_latest_ratios,
    get_profit_loss,
    get_sectors,
)

router = APIRouter(prefix="/companies", tags=["Companies"])


def clean_df(df: pd.DataFrame):
    """Replace NaN values with None across a DataFrame for JSON compatibility."""
    if df is None or df.empty:
        return df

    df = df.astype(object)

    df = df.where(pd.notna(df), None)

    return df.replace({float("nan"): None})


def build_company_dataframe():
    """Build and merge company, sector, and latest financial ratio DataFrames."""

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


@router.get("/")
def list_companies():
    """Retrieve a list of all company records with sector and ratio details."""

    df = build_company_dataframe()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No companies found",
        )

    return clean_df(df).to_dict(orient="records")


@router.get("/{ticker}")
def company_profile(ticker: str):
    """Retrieve the company profile including sector and latest financial ratios."""

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
        latest_ratio = ratios.sort_values("year").iloc[-1].to_dict()

        response["latest_ratio"] = latest_ratio

    return response


@router.get("/{ticker}/pl")
def company_profit_loss(
    ticker: str,
    year: int | None = None,
):
    """Retrieve profit and loss statements for a company."""

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


@router.get("/{ticker}/bs")
def company_balance_sheet(
    ticker: str,
    year: int | None = None,
):
    """Retrieve balance sheet records for a company."""

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


@router.get("/{ticker}/cashflow")
def company_cashflow(
    ticker: str,
    year: int | None = None,
):
    """Retrieve cash flow statements for a company."""

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


@router.get("/{ticker}/ratios")
def company_ratios(
    ticker: str,
    year: int | None = None,
):
    """Retrieve historical financial ratios for a company."""

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


@router.get("/{ticker}/documents")
def company_documents(ticker: str):
    """Retrieve associated documents for a company."""

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


@router.get("/{ticker}/tearsheet")
def company_tearsheet(ticker: str):
    """Download the PDF tearsheet report for a company."""

    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    pdf_path = (
        PROJECT_ROOT / "reports" / "tearsheets" / f"{ticker.upper()}_tearsheet.pdf"
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


@router.get("/ping")
def ping():
    """Return health check ping response for the companies API service."""

    return {
        "status": "ok",
        "service": "companies",
    }
