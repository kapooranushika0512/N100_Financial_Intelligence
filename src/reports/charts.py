from pathlib import Path

import matplotlib.pyplot as plt

OUTPUT = Path("reports/temp")
OUTPUT.mkdir(parents=True, exist_ok=True)


def revenue_profit_chart(pl_df, company):
    """Generate and save a bar/line chart of revenue and net profit trends for a company."""

    _fig, ax = plt.subplots(figsize=(7, 3))

    ax.bar(pl_df["year"], pl_df["sales"], label="Revenue")

    ax.plot(
        pl_df["year"], pl_df["net_profit"], marker="o", linewidth=2, label="Net Profit"
    )

    ax.set_title(f"{company} Revenue vs Net Profit")
    ax.legend()

    file = OUTPUT / f"{company}_rev_profit.png"

    plt.tight_layout()
    plt.savefig(file, dpi=200)
    plt.close()

    return str(file)


def roe_chart(ratio_df, company):
    """Generate and save a line chart showing historical ROE trends for a company."""

    _fig, ax = plt.subplots(figsize=(7, 3))

    ax.plot(ratio_df["year"], ratio_df["return_on_equity_pct"], marker="o", linewidth=2)

    ax.set_title("ROE Trend")

    file = OUTPUT / f"{company}_roe.png"

    plt.tight_layout()
    plt.savefig(file, dpi=200)
    plt.close()

    return str(file)
