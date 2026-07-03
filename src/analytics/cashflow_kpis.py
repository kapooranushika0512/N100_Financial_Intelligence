import csv
import os


def free_cash_flow(
    operating_activity,
    investing_activity
):
    return operating_activity + investing_activity


def cfo_quality_score(
    cfo,
    pat
):
    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(
    investing_activity,
    sales
):
    if sales == 0:
        return None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        return "Asset Light"

    if value <= 8:
        return "Moderate"

    return "Capital Intensive"


def fcf_conversion_rate(
    free_cash_flow_value,
    operating_profit
):
    if operating_profit == 0:
        return None

    return round(
        free_cash_flow_value /
        operating_profit * 100,
        2
    )


def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    quality=None
):

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    if signs == ("+", "-", "-"):
        if quality == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    if signs == ("+", "+", "-"):
        return "Liquidating Assets"

    if signs == ("-", "+", "+"):
        return "Distress Signal"

    if signs == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if signs == ("+", "+", "+"):
        return "Cash Accumulator"

    if signs == ("-", "-", "-"):
        return "Pre-Revenue"

    if signs == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"


def export_capital_allocation(rows):

    os.makedirs(
        "output",
        exist_ok=True
    )

    with open(
        "output/capital_allocation.csv",
        "w",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "company_id",
            "year",
            "cfo_sign",
            "cfi_sign",
            "cff_sign",
            "pattern_label"
        ])

        writer.writerows(rows)