import sqlite3

missing = [
    "ULTRACEMCO",
    "UNIONBANK",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE"
]

conn = sqlite3.connect("db/nifty100.db")

for company in missing:
    conn.execute("""
        INSERT OR IGNORE INTO companies(
            id,
            company_name
        )
        VALUES (?, ?)
    """, (company, company))

conn.commit()
conn.close()

print("Missing companies inserted")