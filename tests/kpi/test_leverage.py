from src.analytics.ratios import *


def test_debt_to_equity():
    """Verify debt_to_equity calculation for non-zero total debt and equity."""

    assert debt_to_equity(100, 50, 50) == 1


def test_debt_free():
    """Verify debt_to_equity returns zero for a debt-free company."""

    assert debt_to_equity(0, 100, 100) == 0


def test_interest_coverage():
    """Verify interest_coverage calculation for valid EBIT and interest expenses."""

    assert interest_coverage(100, 20, 40) == 3


def test_interest_zero():
    """Verify interest_coverage returns None when interest expense is zero."""

    assert interest_coverage(100, 20, 0) is None


def test_icr_label():
    """Verify icr_label identifies a company as Debt Free when coverage is None."""

    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    """Verify icr_warning returns True when interest coverage falls below threshold."""

    assert icr_warning(1.2) is True


def test_high_leverage():
    """Verify high_leverage_flag returns True for high debt relative to sector bounds."""

    assert high_leverage_flag(6, "IT") is True


def test_asset_turnover():
    """Verify asset_turnover correctly computes revenue divided by total assets."""

    assert asset_turnover(200, 100) == 2
