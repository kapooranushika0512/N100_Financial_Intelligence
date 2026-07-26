from pathlib import Path

import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.dashboard.utils.db import (
    get_companies,
    get_latest_ratios,
    get_sectors,
)

styles = getSampleStyleSheet()


def generate_portfolio_summary():
    """Generate a PDF portfolio summary report containing key metrics, top ROE companies, and sector distribution charts."""

    companies = get_companies()
    sectors = get_sectors()
    ratios = get_latest_ratios()

    ratios = ratios.sort_values("year").drop_duplicates(
        subset="company_id", keep="last"
    )

    df = companies.merge(sectors, left_on="id", right_on="company_id", how="left")

    df = df.merge(ratios, on="company_id", how="left")

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    pdf_file = output_dir / "portfolio_summary.pdf"

    doc = SimpleDocTemplate(str(pdf_file))
    story = []

    story.append(
        Paragraph(
            "<b><font size=22>Portfolio Summary Report</font></b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    total_companies = len(df)
    avg_roe = df["return_on_equity_pct"].mean()
    avg_de = df["debt_to_equity"].mean()

    summary = [
        ["Metric", "Value"],
        ["Companies", total_companies],
        ["Average ROE (%)", f"{avg_roe:.2f}"],
        ["Average Debt / Equity", f"{avg_de:.2f}"],
    ]

    table = Table(summary)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("<b>Top 10 Companies by ROE</b>", styles["Heading2"]))

    top = df.sort_values("return_on_equity_pct", ascending=False).head(10)

    top_table = [["Company", "Sector", "ROE"]]

    for _, row in top.iterrows():

        top_table.append(
            [
                row["company_name"],
                row["broad_sector"],
                f"{row['return_on_equity_pct']:.2f}",
            ]
        )

    t = Table(top_table)

    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )

    story.append(t)

    story.append(Spacer(1, 0.35 * inch))

    sector_counts = df["broad_sector"].value_counts().sort_values(ascending=False)

    plt.figure(figsize=(8, 4))
    plt.bar(sector_counts.index, sector_counts.values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Companies")
    plt.tight_layout()

    sector_chart = output_dir / "sector_distribution.png"
    plt.savefig(sector_chart, dpi=200)
    plt.close()

    story.append(
        Paragraph(
            "<b>Sector Distribution</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Image(
            str(sector_chart),
            width=6.5 * inch,
            height=3.5 * inch,
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    plt.figure(figsize=(8, 4))

    plt.hist(
        df["return_on_equity_pct"].dropna(),
        bins=12,
    )

    plt.xlabel("ROE (%)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    roe_chart = output_dir / "roe_distribution.png"

    plt.savefig(roe_chart, dpi=200)
    plt.close()

    story.append(
        Paragraph(
            "<b>ROE Distribution</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Image(
            str(roe_chart),
            width=6.5 * inch,
            height=3.5 * inch,
        )
    )

    doc.build(story)

    print(f"\nPortfolio summary generated at: {pdf_file}")


if __name__ == "__main__":
    generate_portfolio_summary()
