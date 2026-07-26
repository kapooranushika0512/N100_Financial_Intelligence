import pandas as pd
from fastapi import APIRouter, HTTPException

from src.dashboard.utils.db import (
    get_companies,
    get_sectors,
)

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"],
)


def clean_df(df):
    """Replace NaN values with None in a DataFrame for JSON serialization."""

    if df is None or df.empty:
        return df

    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    return df


def build_sector_dataframe():
    """Build and merge sector assignments with company names."""

    sectors = clean_df(get_sectors())
    companies = clean_df(get_companies())

    sectors = sectors.merge(
        companies[["id", "company_name"]],
        left_on="company_id",
        right_on="id",
        how="left",
    )

    sectors.drop(
        columns=["id"],
        inplace=True,
        errors="ignore",
    )

    return clean_df(sectors)


@router.get("/")
def all_sectors():
    """Retrieve sector mapping details across all companies."""

    df = build_sector_dataframe()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Sector data not found",
        )

    return df.to_dict(orient="records")


@router.get("/list")
def sector_list():
    """Retrieve a list of unique broad sectors sorted alphabetically."""

    df = build_sector_dataframe()

    sectors = df["broad_sector"].dropna().sort_values().unique().tolist()

    return sectors


@router.get("/{sector}")
def companies_by_sector(sector: str):
    """Retrieve all companies belonging to a specified broad sector."""

    df = build_sector_dataframe()

    df = df[df["broad_sector"].astype(str).str.lower() == sector.lower()]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{sector} not found",
        )

    return {
        "sector": sector,
        "count": len(df),
        "companies": df.to_dict(orient="records"),
    }


@router.get("/sub/{subsector}")
def companies_by_subsector(subsector: str):
    """Retrieve all companies belonging to a specified sub-sector."""

    df = build_sector_dataframe()

    df = df[df["sub_sector"].astype(str).str.lower() == subsector.lower()]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{subsector} not found",
        )

    return {
        "sub_sector": subsector,
        "count": len(df),
        "companies": df.to_dict(orient="records"),
    }


@router.get("/marketcap/{category}")
def market_cap_category(category: str):
    """Retrieve all companies belonging to a specified market capitalization category."""

    df = build_sector_dataframe()

    df = df[df["market_cap_category"].astype(str).str.lower() == category.lower()]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{category} not found",
        )

    return {
        "category": category,
        "count": len(df),
        "companies": df.to_dict(orient="records"),
    }
