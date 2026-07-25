import sqlite3
import time
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "financial_data.db"

VERSION = "1.0.0"

START_TIME = time.time()

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ---------------------------------------------------
# HEALTH ENDPOINT
# ---------------------------------------------------

@router.get("/health")
def health():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = [
        row["name"]
        for row in cursor.fetchall()
    ]

    row_counts = {}

    for table in tables:

        try:

            cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            row_counts[table] = cursor.fetchone()[0]

        except Exception:

            row_counts[table] = 0

    conn.close()

    uptime = round(
        time.time() - START_TIME,
        2
    )

    return {

        "status": "ok",

        "version": VERSION,

        "uptime_seconds": uptime,

        "db_row_counts": row_counts,

    }