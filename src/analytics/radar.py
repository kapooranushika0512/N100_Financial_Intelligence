import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = "reports/radar_charts"

METRICS = [
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "capex_cr",
]


def load_data():
    ratios = pd.read_excel("data/supporting/financial_ratios.xlsx")
    peers = pd.read_excel("data/supporting/peer_groups.xlsx")

    peers = peers.drop(columns=["id"], errors="ignore")

    df = ratios.merge(
        peers,
        on="company_id",
        how="left"
    )

    return df


def draw_radar(company_row, peer_avg, company_id):

    company = company_row.fillna(0)
    peer = peer_avg.fillna(0)

    values = company.tolist()
    peer_values = peer.tolist()

    angles = np.linspace(
        0,
        2 * np.pi,
        len(METRICS),
        endpoint=False
    )

    angles = np.concatenate((angles, [angles[0]]))

    values += values[:1]
    peer_values += peer_values[:1]

    plt.figure(figsize=(7, 7))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        values,
        linewidth=2,
        label="Company"
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_values,
        "--",
        linewidth=2,
        label="Peer Average"
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        [
            "ROE",
            "OPM",
            "NPM",
            "D/E",
            "ICR",
            "Asset",
            "FCF",
            "CapEx",
        ],
        fontsize=8,
    )

    ax.set_title(
        f"{company_id} Radar Comparison",
        pad=20
    )

    ax.legend(loc="upper right")

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    plt.savefig(
        f"{OUTPUT_DIR}/{company_id}_radar.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()


def run(limit=None):

    df = load_data()

    generated = 0

    for company_id, group in df.groupby("company_id"):

        latest = group.iloc[-1]

        peer_group = latest["peer_group_name"]

        if pd.isna(peer_group):

            peer_average = df[METRICS].mean()

        else:

            peer_average = (
                df[df["peer_group_name"] == peer_group][METRICS]
                .mean()
            )

        draw_radar(
            latest[METRICS],
            peer_average,
            company_id
        )

        generated += 1

        if limit is not None and generated >= limit:
            break

    print(f"Generated {generated} radar charts.")

    return generated


if __name__ == "__main__":
    run()