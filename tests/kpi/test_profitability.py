import pytest

from src.analytics.ratios import *


def test_npm():

    assert net_profit_margin(100,1000)==10


def test_npm_zero_sales():

    assert net_profit_margin(100,0) is None


def test_opm():

    assert operating_profit_margin(250,1000)==25


def test_validate_opm():

    assert validate_opm(20.0,20.5)==True


def test_validate_opm_fail():

    assert validate_opm(20,23)==False


def test_roe():

    assert return_on_equity(100,200,300)==20


def test_negative_equity():

    assert return_on_equity(100,-100,-20) is None


def test_roa():

    assert return_on_assets(100,1000)==10