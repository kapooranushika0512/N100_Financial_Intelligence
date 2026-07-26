import pandas as pd
from loader import load_all_files


def add_failure(failures, table, rule, row_no, severity="CRITICAL"):
    """Append a data quality failure record to the failures list."""

    failures.append({"table": table, "rule": rule, "row": row_no, "severity": severity})


def check_duplicate_id(df, table_name):
    """Validate primary key uniqueness on the 'id' column."""

    failures = []

    if "id" in df.columns:
        dupes = df[df["id"].duplicated()]

        for idx in dupes.index:
            add_failure(failures, table_name, "DQ-01_PK_UNIQUENESS", idx)

    return failures


def check_company_year_duplicate(df, table_name):
    """Validate uniqueness on the composite key (company_id, year)."""

    failures = []

    if "company_id" in df.columns and "year" in df.columns:

        dupes = df[df.duplicated(subset=["company_id", "year"], keep=False)]

        for idx in dupes.index:
            add_failure(failures, table_name, "DQ-02_COMPANY_YEAR_DUPLICATE", idx)

    return failures


def check_null_company_id(df, table_name):
    """Validate foreign key integrity by checking for null company_id values."""

    failures = []

    if "company_id" in df.columns:

        missing = df[df["company_id"].isna()]

        for idx in missing.index:
            add_failure(failures, table_name, "DQ-03_NULL_COMPANY_ID", idx)

    return failures


def check_balance_sheet(df):
    """Validate that total liabilities match total assets within a tolerance threshold."""

    failures = []

    required = ["total_liabilities", "total_assets"]

    if all(col in df.columns for col in required):

        diff = abs(df["total_liabilities"] - df["total_assets"]) / df[
            "total_assets"
        ].replace(0, 1)

        bad_rows = df[diff > 0.01]

        for idx in bad_rows.index:
            add_failure(failures, "balancesheet", "DQ-04_BALANCE_MISMATCH", idx)

    return failures


def check_opm(df):
    """Cross-check reported operating profit margin percentage against calculated OPM."""

    failures = []

    cols = ["sales", "operating_profit", "opm_percentage"]

    if all(col in df.columns for col in cols):

        calc_opm = (df["operating_profit"] / df["sales"].replace(0, 1)) * 100

        diff = abs(calc_opm - df["opm_percentage"])

        bad_rows = df[diff > 2]

        for idx in bad_rows.index:
            add_failure(failures, "profitandloss", "DQ-05_OPM_MISMATCH", idx, "WARNING")

    return failures


def check_positive_sales(df):
    """Validate that all sales values in the profit and loss table are positive."""

    failures = []

    if "sales" in df.columns:

        bad_rows = df[df["sales"] <= 0]

        for idx in bad_rows.index:
            add_failure(failures, "profitandloss", "DQ-06_NON_POSITIVE_SALES", idx)

    return failures


def run_validation():
    """Execute all data quality checks across loaded datasets and output validation failure reports."""

    datasets = load_all_files()

    all_failures = []

    for table_name, df in datasets.items():

        if df is None:
            continue

        all_failures.extend(check_duplicate_id(df, table_name))

        all_failures.extend(check_company_year_duplicate(df, table_name))

        all_failures.extend(check_null_company_id(df, table_name))

        if table_name == "balancesheet":
            all_failures.extend(check_balance_sheet(df))

        if table_name == "profitandloss":
            all_failures.extend(check_opm(df))

            all_failures.extend(check_positive_sales(df))

    failures_df = pd.DataFrame(all_failures)

    failures_df.to_csv("output/validation_failures.csv", index=False)

    print("\nValidation Complete")
    print(f"Total Failures: {len(failures_df)}")


if __name__ == "__main__":
    run_validation()
