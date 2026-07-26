import sqlite3

from loader import load_all_files

DB_PATH = "db/nifty100.db"


def create_database():
    """Initialize SQLite database, apply schema SQL, and load datasets with foreign key validation."""

    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA foreign_keys = ON;")

    with open("db/schema.sql") as f:
        conn.executescript(f.read())

    print("Schema created successfully")

    datasets = load_all_files()

    if "companies" not in datasets:
        raise ValueError("companies dataset not found")

    companies_df = datasets["companies"]

    company_ids = set(companies_df["id"].astype(str).str.strip().str.upper())

    print(f"Companies master count: {len(company_ids)}")

    load_order = [
        "companies",
        "analysis",
        "documents",
        "prosandcons",
        "sectors",
        "peer_groups",
        "cashflow",
        "profitandloss",
        "balancesheet",
        "financial_ratios",
        "market_cap",
        "stock_prices",
    ]

    for table_name in load_order:

        if table_name not in datasets:
            continue

        df = datasets[table_name]

        if df is None:
            continue

        print("\n" + "-" * 50)
        print(f"Processing {table_name}")

        if table_name != "companies" and "company_id" in df.columns:

            df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()

            before = len(df)

            missing_ids = sorted(set(df["company_id"]) - company_ids)

            if missing_ids:

                print(f"Missing company IDs in {table_name}:")

                for x in missing_ids:
                    print(f"  {x}")

            df = df[df["company_id"].isin(company_ids)]

            removed = before - len(df)

            print(f"Removed {removed} FK rows")

        try:

            df.to_sql(table_name, conn, if_exists="append", index=False)

            print(f"Loaded {table_name}: {len(df)} rows")

        except sqlite3.Error as e:

            print(f"\nFAILED TABLE: {table_name}")

            print(f"ERROR: {e}")

            conn.close()

            raise

    conn.commit()

    print("\nDatabase load complete")

    fk_errors = conn.execute("PRAGMA foreign_key_check").fetchall()

    if len(fk_errors) == 0:
        print("Foreign key check PASSED")
    else:
        print(f"Foreign key check FAILED: {len(fk_errors)} errors")

        for row in fk_errors[:20]:
            print(row)

    conn.close()


if __name__ == "__main__":
    create_database()
