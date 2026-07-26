def safe_divide(numerator, denominator):
    """Safely divide two numbers handling division by zero and None values."""

    if denominator is None:
        return None

    if denominator == 0:
        return None

    return numerator / denominator


def net_profit_margin(net_profit, sales):
    """Calculate the net profit margin percentage."""

    result = safe_divide(net_profit, sales)

    if result is None:
        return None

    return round(result * 100, 2)


def operating_profit_margin(operating_profit, sales):
    """Calculate the operating profit margin percentage."""
    result = safe_divide(operating_profit, sales)

    if result is None:
        return None

    return round(result * 100, 2)


def validate_opm(calculated_opm, source_opm):
    """Validate if calculated OPM matches source OPM within tolerance."""
    if calculated_opm is None:
        return False

    if source_opm is None:
        return False

    diff = abs(calculated_opm - source_opm)

    return diff <= 1


def return_on_equity(net_profit, equity_capital, reserves):
    """Calculate return on equity (ROE) percentage."""
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    operating_profit, interest, equity_capital, reserves, borrowings
):
    """Calculate return on capital employed (ROCE) percentage."""

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    ebit = operating_profit + interest

    return round((ebit / capital) * 100, 2)


def return_on_assets(net_profit, total_assets):
    """Calculate return on assets (ROA) percentage."""
    if total_assets <= 0:
        return None

    return round((net_profit / total_assets) * 100, 2)


def debt_to_equity(borrowings, equity_capital, reserves):
    """Calculate the debt to equity ratio."""

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


def high_leverage_flag(debt_equity, broad_sector):
    """Determine if debt to equity ratio exceeds high leverage threshold."""

    if broad_sector == "Financials":
        return False

    return debt_equity > 5


def interest_coverage(operating_profit, other_income, interest):
    """Calculate the interest coverage ratio (ICR)."""

    if interest == 0:
        return None

    return round((operating_profit + other_income) / interest, 2)


def icr_label(icr):
    """Get descriptive status label for the interest coverage ratio."""

    if icr is None:
        return "Debt Free"

    return ""


def icr_warning(icr):
    """Check if interest coverage ratio triggers a risk warning."""

    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    """Calculate net debt by subtracting investments from total borrowings."""

    return borrowings - investments


def asset_turnover(sales, total_assets):
    """Calculate the asset turnover ratio."""

    if total_assets == 0:
        return None

    return round(sales / total_assets, 2)
