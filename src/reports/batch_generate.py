from src.dashboard.utils.db import get_all_company_ids
from src.reports.tearsheet import create_tearsheet


def generate_all_reports():
    """Iterate through all company IDs to generate PDF tearsheet reports and log completion status."""

    companies = get_all_company_ids()

    total = len(companies)

    print(f"\nGenerating {total} company reports...\n")

    success = 0
    failed = []

    for i, company_id in enumerate(companies, start=1):

        try:
            print(f"[{i}/{total}] {company_id}")

            create_tearsheet(company_id)

            success += 1

        except (ValueError, KeyError, TypeError, OSError, RuntimeError) as e:

            print(f"Failed : {company_id}")

            print(e)

            failed.append(company_id)

    print("\n----------------------------")
    print("REPORT GENERATION COMPLETE")
    print("----------------------------")
    print(f"Generated : {success}")
    print(f"Failed    : {len(failed)}")

    if failed:
        print("\nFailed Companies:")
        for company in failed:
            print(company)


if __name__ == "__main__":
    generate_all_reports()
