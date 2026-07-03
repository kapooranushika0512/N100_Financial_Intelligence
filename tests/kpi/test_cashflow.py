from src.analytics.cashflow_kpis import *


def test_fcf():

    assert free_cash_flow(
        100,
        -40
    ) == 60


def test_negative_fcf():

    assert free_cash_flow(
        -20,
        -30
    ) == -50


def test_cfo_quality_high():

    assert cfo_quality_score(
        200,
        100
    ) == "High Quality"


def test_cfo_quality_moderate():

    assert cfo_quality_score(
        60,
        100
    ) == "Moderate"


def test_cfo_quality_low():

    assert cfo_quality_score(
        20,
        100
    ) == "Accrual Risk"


def test_pat_zero():

    assert cfo_quality_score(
        20,
        0
    ) is None


def test_capex():

    assert capex_intensity(
        -20,
        1000
    ) == "Asset Light"


def test_fcf_conversion():

    assert fcf_conversion_rate(
        80,
        100
    ) == 80