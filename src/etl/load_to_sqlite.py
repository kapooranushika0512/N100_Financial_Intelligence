import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "db/nifty100.db"

RAW_PATH = Path("data/raw")
SUPPORTING_PATH = Path("data/supporting")

conn = sqlite3.connect(DB_PATH)

load_audit = []


def load_excel(file_path, header_row):

    df = pd.read_excel(file_path, header=header_row)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    return df


print("\nLOADING CORE FILES")
print("-" * 40)

for file in RAW_PATH.glob("*.xlsx"):

    table_name = file.stem

    df = load_excel(file, 1)

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    print(f"{table_name}: {len(df)} rows")

    load_audit.append(
        [table_name, len(df)]
    )


print("\nLOADING SUPPORTING FILES")
print("-" * 40)

for file in SUPPORTING_PATH.glob("*.xlsx"):

    table_name = file.stem

    df = load_excel(file, 0)

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    print(f"{table_name}: {len(df)} rows")

    load_audit.append(
        [table_name, len(df)]
    )


audit_df = pd.DataFrame(
    load_audit,
    columns=["table_name", "rows_loaded"]
)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

print("\nLoad Complete")
print("Audit Report Created")

conn.close()