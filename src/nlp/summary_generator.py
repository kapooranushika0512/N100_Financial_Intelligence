from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

INPUT_FILE = OUTPUT_DIR / "recommendations.csv"


def load_data():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "recommendations.csv not found. Run Day 31 first."
        )

    return pd.read_csv(INPUT_FILE)


def build_summary(row):

    recommendation = row.recommendation
    confidence = int(row.confidence * 100)

    summary = (
        f"{row.company_id} is rated **{recommendation}** "
        f"with **{confidence}% confidence**. "
    )

    if pd.notna(row.top_pros) and row.top_pros.strip():

        strengths = row.top_pros.replace(";", ",").lower()

        summary += (
            f"The company demonstrates strong financial fundamentals, "
            f"including {strengths}. "
        )

    if pd.notna(row.top_cons) and row.top_cons.strip():

        risk = row.top_cons.lower().strip()

        if "requires further financial monitoring" in risk:

            summary += (
                "Although the overall outlook remains positive, "
                "investors should continue monitoring future financial performance."
            )

        else:

            summary += (
                f"Key risks include {risk}. "
                "Investors should evaluate these factors before making investment decisions."
            )

    else:

        summary += (
            "No major financial concerns were identified based on the available data."
        )

    return summary


def generate():

    df = load_data()

    df["summary"] = df.apply(
        build_summary,
        axis=1,
    )

    df.to_csv(
        OUTPUT_DIR / "summaries.csv",
        index=False,
    )

    print(
        df[
            [
                "company_id",
                "recommendation",
                "summary",
            ]
        ].head(10)
    )

    print()
    print(f"Generated summaries : {len(df)}")


if __name__ == "__main__":
    generate()