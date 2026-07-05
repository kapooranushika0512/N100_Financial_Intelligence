import pandas as pd


def normalize(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series([50] * len(series), index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100


import pandas as pd


def calculate_score(df):

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        df["composite_quality_score"] = 0
        return df

    df["composite_quality_score"] = (
        df[numeric_cols]
        .fillna(0)
        .sum(axis=1)
    )

    return df.sort_values(
        "composite_quality_score",
        ascending=False
    )