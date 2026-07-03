from src.analytics.cashflow_kpis import *

def test_fcf():
    assert free_cash_flow(100, -40) == 60

def test_negative_fcf():
    assert free_cash_flow(-100, -50) == -150

def test_cfo_quality_high():
    assert cfo_quality_score(200, 100) == "High Quality"

def test_cfo_quality_moderate():
    assert cfo_quality_score(75, 100) == "Moderate"

def test_cfo_quality_low():
    assert cfo_quality_score(20, 100) == "Accrual Risk"

def test_pat_zero():
    assert cfo_quality_score(100, 0) is None

def test_capex():
    assert capex_intensity(-20, 200) == 10

def test_fcf_conversion():
    assert fcf_conversion_rate(100, 200) == 50