from pathlib import Path

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
    get_balance_sheet,
    get_cashflow,
    get_company,
    get_company_pros_cons,
    get_company_ratios,
    get_profit_loss,
)

from src.reports.charts import (
    revenue_profit_chart,
    roe_chart,
)

styles = getSampleStyleSheet()


def latest(df):
    if df.empty:
        return None
    return df.iloc[-1]


def value(row, column, suffix=""):
    if row is None:
        return "N/A"

    if column not in row.index:
        return "N/A"

    try:
        return f"{float(row[column]):,.2f}{suffix}"
    except Exception:
        return str(row[column])


def create_tearsheet(company_id):

    company = get_company(company_id)

    if company.empty:
        print(f"{company_id} not found")
        return

    company_name = company.iloc[0]["company_name"]

    pl = get_profit_loss(company_id)
    bs = get_balance_sheet(company_id)
    cf = get_cashflow(company_id)
    ratios = get_company_ratios(company_id)
    proscons = get_company_pros_cons(company_id)

    latest_pl = latest(pl)
    latest_bs = latest(bs)
    latest_ratio = latest(ratios)

    output_dir = Path("reports/tearsheets")
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf = output_dir / f"{company_id}_tearsheet.pdf"

    doc = SimpleDocTemplate(str(pdf))

    story = []

    # ------------------------------------------------
    # TITLE
    # ------------------------------------------------

    story.append(
        Paragraph(
            f"<b><font size='20'>{company_name}</font></b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ------------------------------------------------
    # KPI TABLE
    # ------------------------------------------------

    kpi_data = [
        ["Revenue", value(latest_pl, "sales")],
        ["Net Profit", value(latest_pl, "net_profit")],
        ["ROE", value(latest_ratio, "return_on_equity_pct", "%")],
        ["Debt / Equity", value(latest_ratio, "debt_to_equity")],
        ["EPS", value(latest_pl, "eps")],
        ["Total Assets", value(latest_bs, "total_assets")],
    ]

    table = Table(
        kpi_data,
        colWidths=[2.5 * inch, 2.3 * inch],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D6EAF8")),
                ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))

    # ------------------------------------------------
    # CHARTS
    # ------------------------------------------------

    if not pl.empty:

        revenue_chart = revenue_profit_chart(pl, company_id)

        story.append(
            Image(
                revenue_chart,
                width=6 * inch,
                height=3 * inch,
            )
        )

        story.append(Spacer(1, 0.2 * inch))

    if not ratios.empty:

        roe = roe_chart(ratios, company_id)

        story.append(
            Image(
                roe,
                width=6 * inch,
                height=3 * inch,
            )
        )

        story.append(Spacer(1, 0.3 * inch))

    # ------------------------------------------------
    # PROS
    # ------------------------------------------------

    story.append(
        Paragraph(
            "<b>Pros</b>",
            styles["Heading2"],
        )
    )

    if not proscons.empty:

        for _, row in proscons.head(5).iterrows():

            pro = str(row["pros"]).strip()

            if pro and pro.lower() != "nan":

                story.append(
                    Paragraph(
                        "• " + pro,
                        styles["BodyText"],
                    )
                )

    else:

        story.append(
            Paragraph(
                "No Pros available.",
                styles["BodyText"],
            )
        )

    story.append(Spacer(1, 0.25 * inch))

    # ------------------------------------------------
    # CONS
    # ------------------------------------------------

    story.append(
        Paragraph(
            "<b>Cons</b>",
            styles["Heading2"],
        )
    )

    if not proscons.empty:

        for _, row in proscons.head(5).iterrows():

            con = str(row["cons"]).strip()

            if con and con.lower() != "nan":

                story.append(
                    Paragraph(
                        "• " + con,
                        styles["BodyText"],
                    )
                )

    else:

        story.append(
            Paragraph(
                "No Cons available.",
                styles["BodyText"],
            )
        )

    # ------------------------------------------------
    # BUILD PDF
    # ------------------------------------------------

    doc.build(story)

    print(f"Generated: {pdf}")


if __name__ == "__main__":
    create_tearsheet("TCS")