import pandas as pd
from loader import load_all_files


def check_null_company_id(df, table_name):

    if "company_id" not in df.columns:
        return []

    failures = []

    missing = df[df["company_id"].isna()]

    for index, row in missing.iterrows():

        failures.append({
            "table": table_name,
            "rule": "NULL_COMPANY_ID",
            "row": index
        })

    return failures


def check_duplicate_id(df, table_name):

    if "id" not in df.columns:
        return []

    failures = []

    duplicates = df[df["id"].duplicated()]

    for index, row in duplicates.iterrows():

        failures.append({
            "table": table_name,
            "rule": "DUPLICATE_ID",
            "row": index
        })

    return failures


def run_validation():

    datasets = load_all_files()

    all_failures = []

    for table_name, df in datasets.items():

        if df is None:
            continue

        all_failures.extend(
            check_null_company_id(df, table_name)
        )

        all_failures.extend(
            check_duplicate_id(df, table_name)
        )

    failures_df = pd.DataFrame(all_failures)

    failures_df.to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print("\nValidation Complete")

    print(
        f"Total Failures: {len(failures_df)}"
    )


if __name__ == "__main__":

    run_validation()