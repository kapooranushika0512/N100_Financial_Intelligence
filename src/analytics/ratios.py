import math
def safe_divide(numerator, denominator):

    if denominator is None:
        return None

    if denominator == 0:
        return None

    return numerator / denominator

def net_profit_margin(net_profit, sales):

    result = safe_divide(net_profit, sales)

    if result is None:
        return None

    return round(result * 100, 2)
def operating_profit_margin(operating_profit, sales):
    result = safe_divide(operating_profit, sales)

    if result is None:
        return None

    return round(result * 100, 2)

def validate_opm(calculated_opm, source_opm):
    if calculated_opm is None:
        return False

    if source_opm is None:
        return False

    diff = abs(calculated_opm - source_opm)

    return diff <= 1

def return_on_equity(
    net_profit,
    equity_capital,
    reserves
):
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(
        (net_profit / equity) * 100,
        2
    )


def return_on_capital_employed(
    operating_profit,
    interest,
    equity_capital,
    reserves,
    borrowings
):

    capital = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital <= 0:
        return None

    ebit = operating_profit + interest

    return round(
        (ebit / capital) * 100,
        2
    )


def return_on_assets(
    net_profit,
    total_assets
):
    if total_assets <= 0:
        return None

    return round(
        (net_profit / total_assets) * 100,
        2
    )
def debt_to_equity(
    borrowings,
    equity_capital,
    reserves
):

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(
        borrowings / equity,
        2
    )


def high_leverage_flag(
    debt_equity,
    broad_sector
):

    if broad_sector == "Financials":
        return False

    return debt_equity > 5


def interest_coverage(
    operating_profit,
    other_income,
    interest
):

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income)
        / interest,
        2
    )


def icr_label(icr):

    if icr is None:
        return "Debt Free"

    return ""


def icr_warning(icr):

    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings,
    investments
):

    return borrowings - investments


def asset_turnover(
    sales,
    total_assets
):

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2
    )