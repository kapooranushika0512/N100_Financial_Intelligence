import os
import sqlite3

OUTPUT_FILES = ["output/screener_output.xlsx", "output/peer_comparison.xlsx"]

RADAR_FOLDER = "reports/radar_charts"
DB_PATH = "db/nifty100.db"


def check_outputs():
    """Verify the existence of required output files and radar charts directory."""

    print("\nChecking generated outputs...\n")

    for file in OUTPUT_FILES:

        if os.path.exists(file):
            print(f"PASS - {file}")
        else:
            print(f"FAIL - {file} not found")

    if os.path.isdir(RADAR_FOLDER):

        total = len(os.listdir(RADAR_FOLDER))
        print(f"PASS - Radar charts generated ({total} files)")

    else:

        print("FAIL - Radar charts folder missing")


def check_database():
    """Check and log the row count for the peer_percentiles database table."""

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM peer_percentiles")

    rows = cur.fetchone()[0]

    print(f"\npeer_percentiles rows : {rows}")

    conn.close()


def run():
    """Execute the Sprint 3 output and database review pipeline."""

    print("\n========== Sprint 3 Review ==========\n")

    check_outputs()

    check_database()

    print("\nSprint 3 validation completed.\n")


if __name__ == "__main__":
    run()
