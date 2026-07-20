from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

PROS_CONS_FILE = OUTPUT_DIR / "pros_cons_generated.csv"


def load_pros_cons():

    if not PROS_CONS_FILE.exists():
        raise FileNotFoundError(
            "pros_cons_generated.csv not found. Run Day 30 first."
        )

    return pd.read_csv(PROS_CONS_FILE)


def get_recommendation(score):

    if score >= 3.5:
        return "Strong Buy", 0.95

    elif score >= 2.0:
        return "Buy", 0.90

    elif score >= 0.5:
        return "Hold", 0.85

    elif score >= -1.0:
        return "Sell", 0.80

    return "Avoid", 0.95


def generate():

    df = load_pros_cons()

    results = []

    companies = sorted(df.company_id.unique())

    for company in companies:

        company_df = df[df.company_id == company]

        pros_df = company_df[company_df.type == "Pro"]
        cons_df = company_df[company_df.type == "Con"]

        pros = len(pros_df)
        cons = len(cons_df)

        score = (
            pros_df["confidence"].sum()
            - cons_df["confidence"].sum()
        )

        recommendation, confidence = get_recommendation(score)

        top_pros = (
            pros_df
            .head(2)["reason"]
            .tolist()
        )

        top_cons = (
            cons_df
            .head(2)["reason"]
            .tolist()
        )

        results.append(
            {
                "company_id": company,
                "pros": pros,
                "cons": cons,
                "score": round(score, 2),
                "recommendation": recommendation,
                "confidence": confidence,
                "top_pros": "; ".join(top_pros),
                "top_cons": "; ".join(top_cons),
            }
        )

    recommendations = pd.DataFrame(results)

    recommendations = recommendations.sort_values(
        ["score", "company_id"],
        ascending=[False, True]
    )

    recommendations.to_csv(
        OUTPUT_DIR / "recommendations.csv",
        index=False,
    )

    print(recommendations.head(10))

    print()
    print(f"Companies processed : {len(recommendations)}")

    print()

    print(
        recommendations["recommendation"]
        .value_counts()
    )


if __name__ == "__main__":
    generate()