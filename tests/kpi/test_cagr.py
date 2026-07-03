from src.analytics.cagr import *


def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        200,
        5
    )

    assert flag == "OK"


def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        100,
        5
    )

    assert flag == "TURNAROUND"


def test_decline():

    value, flag = calculate_cagr(
        100,
        -100,
        5
    )

    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -50,
        5
    )

    assert flag == "BOTH_NEGATIVE"


def test_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        5
    )

    assert flag == "ZERO_BASE"


def test_insufficient():

    value, flag = calculate_cagr(
        100,
        200,
        2
    )

    assert flag == "INSUFFICIENT"


def test_none_start():

    value, flag = calculate_cagr(
        None,
        100,
        5
    )

    assert value is None


def test_none_end():

    value, flag = calculate_cagr(
        100,
        None,
        5
    )

    assert value is None


def test_revenue_cagr():

    value, flag = revenue_cagr(
        100,
        200,
        5
    )

    assert flag == "OK"


def test_eps_cagr():

    value, flag = eps_cagr(
        10,
        20,
        5
    )

    assert flag == "OK"