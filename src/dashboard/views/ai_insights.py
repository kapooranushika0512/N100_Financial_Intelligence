from pathlib import Path

import pandas as pd
import streamlit as st

OUTPUT_DIR = Path("output")

PROS_FILE = OUTPUT_DIR / "pros_cons_generated.csv"
REC_FILE = OUTPUT_DIR / "recommendations.csv"
SUMMARY_FILE = OUTPUT_DIR / "summaries.csv"


@st.cache_data
def load_data():

    if (
        not PROS_FILE.exists()
        or not REC_FILE.exists()
        or not SUMMARY_FILE.exists()
    ):
        st.error(
            "AI analysis files are missing.\n\n"
            "Please run:\n"
            "• python -m src.nlp.pros_cons_generator\n"
            "• python -m src.nlp.recommendation_engine\n"
            "• python -m src.nlp.summary_generator"
        )
        st.stop()

    pros = pd.read_csv(PROS_FILE)
    recommendations = pd.read_csv(REC_FILE)
    summaries = pd.read_csv(SUMMARY_FILE)

    return pros, recommendations, summaries


def recommendation_banner(rec):

    if rec == "Strong Buy":
        st.success(
            "🟢 **Strong Buy** — Excellent financial fundamentals with strong long-term investment potential."
        )

    elif rec == "Buy":
        st.success(
            "🟢 **Buy** — Strong financial health and positive growth indicators."
        )

    elif rec == "Hold":
        st.warning(
            "🟡 **Hold** — Stable company. Continue monitoring future performance."
        )

    elif rec == "Sell":
        st.warning(
            "🟠 **Sell** — Financial indicators suggest caution."
        )

    else:
        st.error(
            "🔴 **Avoid** — Weak financial performance and elevated investment risk."
        )


def show():

    st.title("🤖 AI Investment Insights")

    st.caption(
        "AI-powered investment analysis generated using financial ratios, "
        "annual report insights, NLP parsing, and a rule-based recommendation engine."
    )

    pros, rec, summaries = load_data()

    company = st.selectbox(
        "🏢 Select Company",
        sorted(rec.company_id.unique()),
    )

    recommendation = rec[
        rec.company_id == company
    ].iloc[0]

    summary = summaries[
        summaries.company_id == company
    ].iloc[0]

    ranking = (
        rec.sort_values(
            "score",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    company_rank = (
        ranking.index[
            ranking.company_id == company
        ][0]
        + 1
    )

    pros_df = pros[
        (pros.company_id == company)
        &
        (pros.type == "Pro")
    ].sort_values(
        "confidence",
        ascending=False,
    )

    cons_df = pros[
        (pros.company_id == company)
        &
        (pros.type == "Con")
    ].sort_values(
        "confidence",
        ascending=False,
    )

    st.divider()

    recommendation_banner(
        recommendation.recommendation
    )

    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Recommendation",
            recommendation.recommendation,
        )

    with c2:
        st.metric(
            "Confidence",
            f"{int(recommendation.confidence * 100)}%",
        )

        st.progress(
            float(recommendation.confidence)
        )

    with c3:
        st.metric(
            "Positive Signals",
            int(recommendation.pros),
        )

    with c4:
        st.metric(
            "Risk Signals",
            int(recommendation.cons),
        )

    with c5:
        st.metric(
            "Overall Rank",
            f"#{company_rank}",
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("✅ Top Strengths")

        if pros_df.empty:

            st.info(
                "No significant strengths detected."
            )

        else:

            for _, row in pros_df.head(5).iterrows():

                st.success(
                    f"**{row.reason}**\n\n"
                    f"Confidence: {int(row.confidence * 100)}%"
                )

    with right:

        st.subheader("⚠️ Key Risks")

        if cons_df.empty:

            st.success(
                "No major concerns detected."
            )

        else:

            for _, row in cons_df.head(5).iterrows():

                st.error(
                    f"**{row.reason}**\n\n"
                    f"Confidence: {int(row.confidence * 100)}%"
                )

    st.divider()

    with st.expander(
        "📝 AI Investment Summary",
        expanded=True,
    ):

        st.write(summary.summary)

    st.divider()

    st.subheader("📥 Export AI Analysis")

    col1, col2 = st.columns(2)

    with col1:

        with open(REC_FILE, "rb") as file:

            st.download_button(
                label="⬇️ Download Recommendations",
                data=file,
                file_name="recommendations.csv",
                mime="text/csv",
            )

    with col2:

        with open(SUMMARY_FILE, "rb") as file:

            st.download_button(
                label="⬇️ Download AI Summaries",
                data=file,
                file_name="summaries.csv",
                mime="text/csv",
            )

    st.divider()

    st.caption(
        "📌 Recommendations are automatically generated using "
        "financial ratios, parsed annual reports, NLP-based insight extraction, "
        "confidence-weighted scoring, and a rule-based AI recommendation engine."
    )