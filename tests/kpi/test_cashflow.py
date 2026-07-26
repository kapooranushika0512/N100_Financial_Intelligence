from src.analytics.cashflow_kpis import *


def test_fcf():
    """Verify free_cash_flow calculation with positive cash flow and capital expenditure."""

    assert free_cash_flow(100, -40) == 60


def test_negative_fcf():
    """Verify free_cash_flow calculation when operating cash flow is negative."""

    assert free_cash_flow(-20, -30) == -50


def test_cfo_quality_high():
    """Verify cfo_quality_score returns High Quality for cash flow exceeding PAT."""

    assert cfo_quality_score(200, 100) == "High Quality"


def test_cfo_quality_moderate():
    """Verify cfo_quality_score returns Moderate when cash flow is in the medium range relative to PAT."""

    assert cfo_quality_score(60, 100) == "Moderate"


def test_cfo_quality_low():
    """Verify cfo_quality_score flags Accrual Risk when cash flow is low relative to PAT."""

    assert cfo_quality_score(20, 100) == "Accrual Risk"


def test_pat_zero():
    """Verify cfo_quality_score returns None when PAT is zero."""

    assert cfo_quality_score(20, 0) is None


def test_capex():
    """Verify capex_intensity classifies low capex relative to revenue as Asset Light."""

    assert capex_intensity(-20, 1000) == "Asset Light"


def test_fcf_conversion():
    """Verify fcf_conversion_rate correctly calculates FCF as a percentage of PAT."""

    assert fcf_conversion_rate(80, 100) == 80
