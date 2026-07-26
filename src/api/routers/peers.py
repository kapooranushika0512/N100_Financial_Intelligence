import pandas as pd
from fastapi import APIRouter, HTTPException

from src.dashboard.utils.db import (
    get_company_peer,
    get_peer_companies,
    get_peer_group,
    get_peer_groups,
    get_peer_percentiles,
)

router = APIRouter(
    prefix="/peers",
    tags=["Peers"],
)


def clean_df(df):
    """Replace NaN values with None in a DataFrame for JSON serialization."""

    if df is None or df.empty:
        return df

    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    return df


@router.get("/")
def peer_groups():
    """Retrieve all peer group records."""

    df = clean_df(get_peer_groups())

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Peer groups not found",
        )

    return df.to_dict(orient="records")


@router.get("/groups")
def peer_group_names():
    """Retrieve a list of unique peer group names sorted alphabetically."""

    df = clean_df(get_peer_groups())

    groups = df["peer_group_name"].dropna().sort_values().unique().tolist()

    return groups


@router.get("/group/{group}")
def peer_group(group: str):
    """Retrieve all companies belonging to a specified peer group."""

    df = clean_df(get_peer_group(group))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{group} not found",
        )

    return {
        "peer_group": group,
        "count": len(df),
        "companies": df.to_dict(orient="records"),
    }


@router.get("/company/{ticker}")
def company_peers(ticker: str):
    """Retrieve peer mapping information for a specific company ticker."""

    df = clean_df(get_company_peer(ticker))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{ticker} not found",
        )

    return df.to_dict(orient="records")


@router.get("/companies/{group}")
def peer_companies(group: str):
    """Retrieve detailed company profiles belonging to a specific peer group."""

    df = clean_df(get_peer_companies(group))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{group} not found",
        )

    return {
        "peer_group": group,
        "count": len(df),
        "companies": df.to_dict(orient="records"),
    }


@router.get("/percentiles")
def percentiles():
    """Retrieve peer percentile rankings for all tracked companies and metrics."""

    df = clean_df(get_peer_percentiles())

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Percentiles not found",
        )

    return df.to_dict(orient="records")
