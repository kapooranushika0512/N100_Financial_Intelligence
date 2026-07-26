from src.analytics.cagr import *


def test_normal_cagr():
    """Verify calculate_cagr returns OK status for positive initial and final values."""

    _, flag = calculate_cagr(100, 200, 5)

    assert flag == "OK"


def test_turnaround():
    """Verify calculate_cagr detects turnaround when starting negative and ending positive."""

    _, flag = calculate_cagr(-100, 100, 5)

    assert flag == "TURNAROUND"


def test_decline():
    """Verify calculate_cagr flags a transition from positive to negative as DECLINE_TO_LOSS."""

    _, flag = calculate_cagr(100, -100, 5)

    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():
    """Verify calculate_cagr returns BOTH_NEGATIVE when both initial and final values are negative."""

    _, flag = calculate_cagr(-100, -50, 5)

    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    """Verify calculate_cagr flags a calculation with a starting value of zero as ZERO_BASE."""

    _, flag = calculate_cagr(0, 100, 5)

    assert flag == "ZERO_BASE"


def test_insufficient():
    """Verify calculate_cagr flags period lengths shorter than minimum as INSUFFICIENT."""

    _, flag = calculate_cagr(100, 200, 2)

    assert flag == "INSUFFICIENT"


def test_none_start():
    """Verify calculate_cagr returns None value when initial value is None."""

    value, _ = calculate_cagr(None, 100, 5)

    assert value is None


def test_none_end():
    """Verify calculate_cagr returns None value when final value is None."""

    value, _ = calculate_cagr(100, None, 5)

    assert value is None


def test_revenue_cagr():
    """Verify revenue_cagr returns OK status for valid revenue growth."""

    _, flag = revenue_cagr(100, 200, 5)

    assert flag == "OK"


def test_eps_cagr():
    """Verify eps_cagr returns OK status for valid earnings per share growth."""

    _, flag = eps_cagr(10, 20, 5)

    assert flag == "OK"
