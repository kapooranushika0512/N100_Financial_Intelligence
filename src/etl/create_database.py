import sqlite3

conn = sqlite3.connect("db/nifty100.db")

with open("db/schema.sql", "r") as f:
    conn.executescript(f.read())

print("Schema created successfully")

conn.close()