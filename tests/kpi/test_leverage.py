from src.analytics.ratios import *


def test_debt_to_equity():

    assert debt_to_equity(
        100,
        50,
        50
    ) == 1


def test_debt_free():

    assert debt_to_equity(
        0,
        100,
        100
    ) == 0


def test_interest_coverage():

    assert interest_coverage(
        100,
        20,
        40
    ) == 3


def test_interest_zero():

    assert interest_coverage(
        100,
        20,
        0
    ) is None


def test_icr_label():

    assert icr_label(None) == "Debt Free"


def test_icr_warning():

    assert icr_warning(1.2) is True


def test_high_leverage():

    assert high_leverage_flag(
        6,
        "IT"
    ) is True


def test_asset_turnover():

    assert asset_turnover(
        200,
        100
    ) == 2