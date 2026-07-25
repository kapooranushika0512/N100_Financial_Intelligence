from fastapi import APIRouter, HTTPException
import pandas as pd

from src.dashboard.utils.db import (
    get_peer_groups,
    get_peer_group,
    get_company_peer,
    get_peer_percentiles,
    get_peer_companies,
)

router = APIRouter(
    prefix="/peers",
    tags=["Peers"],
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
# ALL PEER GROUPS
# ---------------------------------------------------------

@router.get("/")
def peer_groups():

    df = clean_df(get_peer_groups())

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Peer groups not found",
        )

    return df.to_dict(orient="records")


# ---------------------------------------------------------
# UNIQUE GROUPS
# ---------------------------------------------------------

@router.get("/groups")
def peer_group_names():

    df = clean_df(get_peer_groups())

    groups = (
        df["peer_group_name"]
        .dropna()
        .sort_values()
        .unique()
        .tolist()
    )

    return groups


# ---------------------------------------------------------
# SINGLE PEER GROUP
# ---------------------------------------------------------

@router.get("/group/{group}")
def peer_group(group: str):

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


# ---------------------------------------------------------
# COMPANY PEERS
# ---------------------------------------------------------

@router.get("/company/{ticker}")
def company_peers(ticker: str):

    df = clean_df(get_company_peer(ticker))

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"{ticker} not found",
        )

    return df.to_dict(orient="records")


# ---------------------------------------------------------
# PEER COMPANIES
# ---------------------------------------------------------

@router.get("/companies/{group}")
def peer_companies(group: str):

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


# ---------------------------------------------------------
# PEER PERCENTILES
# ---------------------------------------------------------

@router.get("/percentiles")
def percentiles():

    df = clean_df(get_peer_percentiles())

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Percentiles not found",
        )

    return df.to_dict(orient="records")