import warnings
warnings.filterwarnings("ignore")

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.dashboard.utils.db import (
    get_companies,
    get_latest_ratios,
    get_sectors,
    get_analysis,
)

# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "output"
REPORT_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# FEATURES USED FOR CLUSTERING
# ---------------------------------------------------

FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "compounded_sales_growth",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
]
def load_data():

    companies = get_companies()

    ratios = get_latest_ratios()

    sectors = get_sectors()

    analysis = get_analysis()

    # keep only required columns

    companies = companies[
        [
            "id",
            "company_name",
        ]
    ]

    sectors = sectors[
        [
            "company_id",
            "broad_sector",
        ]
    ]

    analysis = analysis[
        [
            "company_id",
            "compounded_sales_growth",
        ]
    ]

    # merge latest ratios

    df = companies.merge(
        ratios,
        left_on="id",
        right_on="company_id",
        how="left",
    )

    # merge sectors

    df = df.merge(
        sectors,
        on="company_id",
        how="left",
    )

    # merge analysis

    df = df.merge(
        analysis,
        on="company_id",
        how="left",
    )

    return df
def sector_imputation(df):

    # Convert every feature to numeric
    for feature in FEATURES:
        df[feature] = pd.to_numeric(
            df[feature],
            errors="coerce"
        )

    for feature in FEATURES:

        sector_median = (
            df.groupby("broad_sector")[feature]
            .transform("median")
        )

        df[feature] = df[feature].fillna(sector_median)

        overall = df[feature].median()

        if pd.isna(overall):
            overall = 0

        df[feature] = df[feature].fillna(overall)

    return df
def preprocess(df):

    df = sector_imputation(df)

    # Safety conversion
    for feature in FEATURES:
        df[feature] = pd.to_numeric(
            df[feature],
            errors="coerce"
        )

    # Fill any remaining NaNs
    for feature in FEATURES:

        median = df[feature].median()

        if pd.isna(median):
            median = 0

        df[feature] = df[feature].fillna(median)

    print("\nMissing values after preprocessing:")
    print(df[FEATURES].isna().sum())

    scaler = StandardScaler()

    X = scaler.fit_transform(df[FEATURES])

    return df, X, scaler
# ---------------------------------------------------
# ELBOW METHOD
# ---------------------------------------------------

def generate_elbow_plot(X):

    inertias = []

    for k in range(2, 11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )

        model.fit(X)

        inertias.append(model.inertia_)

    plt.figure(figsize=(8, 5))

    plt.plot(
        range(2, 11),
        inertias,
        marker="o",
        linewidth=2,
    )

    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.title("KMeans Elbow Plot")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        REPORT_DIR / "elbow_plot.png",
        dpi=300,
    )

    plt.close()
# ---------------------------------------------------
# CLUSTER NAMES
# ---------------------------------------------------

def assign_cluster_names(profile):

    names = {}

    for cluster in profile.index:

        row = profile.loc[cluster]

        roe = row["return_on_equity_pct"]

        growth = row["compounded_sales_growth"]

        debt = row["debt_to_equity"]

        opm = row["operating_profit_margin_pct"]

        if roe > 20 and growth > 15:
            names[cluster] = "High Growth Leaders"

        elif debt < 0.5 and opm > 20:
            names[cluster] = "Stable Compounders"

        elif debt > 1.5:
            names[cluster] = "Highly Leveraged"

        elif growth < 5:
            names[cluster] = "Mature Businesses"

        else:
            names[cluster] = "Balanced Performers"

    return names
# ---------------------------------------------------
# KMEANS
# ---------------------------------------------------

def perform_clustering(df, X):

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=20,
    )

    df["cluster_id"] = model.fit_predict(X)

    distances = model.transform(X)

    df["distance_from_centroid"] = distances.min(axis=1)

    profile = (
        df.groupby("cluster_id")[FEATURES]
        .mean()
        .round(2)
    )

    cluster_names = assign_cluster_names(profile)

    df["cluster_name"] = (
        df["cluster_id"]
        .map(cluster_names)
    )

    return df, profile
# ---------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------

def save_cluster_labels(df):

    output = df[
        [
            "company_id",
            "company_name",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid",
        ]
    ].sort_values(
        ["cluster_id", "company_name"]
    )

    output.to_csv(
        OUTPUT_DIR / "cluster_labels.csv",
        index=False,
    )

    print("\nCluster labels saved.")

    print(output.head())


def save_cluster_profile(profile):

    profile.to_csv(
        OUTPUT_DIR / "cluster_profile.csv"
    )

    print("\nCluster profile saved.")
# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():

    print("=" * 60)
    print("Financial Intelligence - Day 36")
    print("=" * 60)

    print("\nLoading data...")

    df = load_data()

    print("\nFeature Data Types:")
    print(df[FEATURES].dtypes)

    print(f"\nCompanies : {len(df)}")

    print("\nPreprocessing...")

    df, X, scaler = preprocess(df)

    print("Generating elbow plot...")

    generate_elbow_plot(X)

    print("Running KMeans...")

    df, profile = perform_clustering(df, X)

    save_cluster_labels(df)

    save_cluster_profile(profile)

    print("\nCluster Summary\n")

    print(
        df.groupby("cluster_name")
        .size()
        .sort_values(ascending=False)
    )

    print("\nDay 36 Completed Successfully!")
    print(f"Elbow Plot        : {REPORT_DIR/'elbow_plot.png'}")
    print(f"Cluster Labels    : {OUTPUT_DIR/'cluster_labels.csv'}")
    print(f"Cluster Profile   : {OUTPUT_DIR/'cluster_profile.csv'}")


# ---------------------------------------------------

if __name__ == "__main__":
    main()