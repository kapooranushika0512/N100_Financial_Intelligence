import sqlite3
import time
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "financial_data.db"

VERSION = "1.0.0"

START_TIME = time.time()


def get_connection():
    """Establish and return an SQLite database connection with row factory configured."""

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


@router.get("/health")
def health():
    """Return API health status, version, uptime, and database row counts."""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """)

    tables = [row["name"] for row in cursor.fetchall()]

    row_counts = {}

    for table in tables:

        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_counts[table] = cursor.fetchone()[0]

        except sqlite3.Error:
            row_counts[table] = 0

    conn.close()

    uptime = round(time.time() - START_TIME, 2)

    return {
        "status": "ok",
        "version": VERSION,
        "uptime_seconds": uptime,
        "db_row_counts": row_counts,
    }
