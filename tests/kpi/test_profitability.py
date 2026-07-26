from src.analytics.ratios import *


def test_npm():
    """Verify net_profit_margin correctly calculates percentage margin."""

    assert net_profit_margin(100, 1000) == 10


def test_npm_zero_sales():
    """Verify net_profit_margin returns None when sales are zero."""

    assert net_profit_margin(100, 0) is None


def test_opm():
    """Verify operating_profit_margin correctly calculates operating margin percentage."""

    assert operating_profit_margin(250, 1000) == 25


def test_validate_opm():
    """Verify validate_opm returns True when values are within acceptable tolerance."""

    assert validate_opm(20.0, 20.5) == True


def test_validate_opm_fail():
    """Verify validate_opm returns False when margin variance exceeds threshold."""

    assert validate_opm(20, 23) == False


def test_roe():
    """Verify return_on_equity correctly calculates ROE using average equity."""

    assert return_on_equity(100, 200, 300) == 20


def test_negative_equity():
    """Verify return_on_equity returns None when average equity is negative."""

    assert return_on_equity(100, -100, -20) is None


def test_roa():
    """Verify return_on_assets correctly calculates ROA from net income and total assets."""

    assert return_on_assets(100, 1000) == 10
