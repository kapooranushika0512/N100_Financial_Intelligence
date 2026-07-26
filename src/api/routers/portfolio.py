import pandas as pd
from fastapi import APIRouter, HTTPException

from src.dashboard.utils.db import get_latest_ratios

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


def clean_df(df):
    """Replace NaN values with None in a DataFrame for JSON serialization."""

    if df is None or df.empty:
        return df

    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    return df


@router.get("/stats")
def portfolio_stats():
    """Calculate statistical summaries and percentiles for portfolio metrics."""

    df = get_latest_ratios()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Portfolio data not found",
        )

    df = clean_df(df)

    numeric_columns = []

    for col in df.columns:

        if col in ["company_id", "year"]:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_columns.append(col)

    stats = []

    for col in numeric_columns:

        series = pd.to_numeric(df[col], errors="coerce").dropna()

        if series.empty:
            continue

        stats.append(
            {
                "metric": col,
                "P10": round(series.quantile(0.10), 2),
                "P25": round(series.quantile(0.25), 2),
                "P50": round(series.quantile(0.50), 2),
                "P75": round(series.quantile(0.75), 2),
                "P90": round(series.quantile(0.90), 2),
                "Mean": round(series.mean(), 2),
                "Std": round(series.std(), 2),
            }
        )

    return {
        "total_companies": len(df),
        "metrics": stats,
    }


@router.get("/")
def portfolio_summary():
    """Retrieve summary metadata for the current portfolio dataset."""

    df = get_latest_ratios()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Portfolio data not found",
        )

    return {
        "companies": len(df),
        "available_metrics": len(df.columns),
        "latest_year": int(df["year"].max()),
    }
