from pathlib import Path

import matplotlib.pyplot as plt

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
from reportlab.lib import colors

from src.dashboard.utils.db import (
    get_companies,
    get_latest_ratios,
    get_sectors,
)

styles = getSampleStyleSheet()


def generate_sector_report():

    companies = get_companies()
    sectors = get_sectors()
    ratios = get_latest_ratios()

    # Keep one latest ratio row per company
    ratios = (
        ratios.sort_values("year")
        .drop_duplicates(subset="company_id", keep="last")
    )

    # Merge company + sector
    df = companies.merge(
        sectors,
        left_on="id",
        right_on="company_id",
        how="left"
    )

    # Merge ratios
    df = df.merge(
        ratios,
        on="company_id",
        how="left"
    )

    output_dir = Path("reports/sector_reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    sector_list = sorted(df["broad_sector"].dropna().unique())

    print(f"Generating {len(sector_list)} reports...")

    for sector in sector_list:

        sector_df = df[df["broad_sector"] == sector].copy()

        pdf = output_dir / f"{sector}.pdf"

        doc = SimpleDocTemplate(str(pdf))
        story = []

        story.append(
            Paragraph(
                f"<b><font size=20>{sector} Sector Report</font></b>",
                styles["Title"],
            )
        )

        story.append(Spacer(1, 0.3 * inch))

        avg_roe = sector_df["return_on_equity_pct"].mean()
        avg_de = sector_df["debt_to_equity"].mean()

        table_data = [
            ["Metric", "Value"],
            ["Companies", len(sector_df)],
            ["Average ROE", f"{avg_roe:.2f}%"],
            ["Average Debt/Equity", f"{avg_de:.2f}"],
        ]

        table = Table(table_data)
        table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, colors.black),
            ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ]))

        story.append(table)
        story.append(Spacer(1, 0.3 * inch))

        top = sector_df.sort_values(
            "return_on_equity_pct",
            ascending=False
        ).head(10)

        plt.figure(figsize=(8,3))
        plt.bar(top["company_name"], top["return_on_equity_pct"])
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("ROE %")
        plt.tight_layout()

        chart = output_dir / f"{sector}.png"
        plt.savefig(chart, dpi=200)
        plt.close()

        story.append(Image(str(chart), width=6.5*inch, height=3*inch))

        doc.build(story)

        print(f"✓ {sector}")

    print("Done!")


if __name__ == "__main__":
    generate_sector_report()