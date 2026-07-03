import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src" / "etl"))

from normaliser import normalize_ticker, normalize_year


# ------------------------
# normalize_ticker tests
# ------------------------

def test_ticker_1():
    assert normalize_ticker("abb") == "ABB"

def test_ticker_2():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_3():
    assert normalize_ticker("infy") == "INFY"

def test_ticker_4():
    assert normalize_ticker(" hdfcbank ") == "HDFCBANK"

def test_ticker_5():
    assert normalize_ticker("reliance") == "RELIANCE"

def test_ticker_6():
    assert normalize_ticker("sbin") == "SBIN"

def test_ticker_7():
    assert normalize_ticker("itc") == "ITC"

def test_ticker_8():
    assert normalize_ticker("asianpaint") == "ASIANPAINT"

def test_ticker_9():
    assert normalize_ticker("kotakbank") == "KOTAKBANK"

def test_ticker_10():
    assert normalize_ticker("axisbank") == "AXISBANK"

def test_ticker_11():
    assert normalize_ticker("wipro") == "WIPRO"

def test_ticker_12():
    assert normalize_ticker("ultracemco") == "ULTRACEMCO"

def test_ticker_13():
    assert normalize_ticker("nestleind") == "NESTLEIND"

def test_ticker_14():
    assert normalize_ticker("bajajauto") == "BAJAJAUTO"

def test_ticker_15():
    assert normalize_ticker("sunpharma") == "SUNPHARMA"


# ------------------------
# normalize_year tests
# ------------------------

def test_year_1():
    assert normalize_year("Mar 2024") == "Mar 2024"

def test_year_2():
    assert normalize_year("Mar 2023") == "Mar 2023"

def test_year_3():
    assert normalize_year("Mar 2022") == "Mar 2022"

def test_year_4():
    assert normalize_year("Mar 2021") == "Mar 2021"

def test_year_5():
    assert normalize_year("Mar 2020") == "Mar 2020"

def test_year_6():
    assert normalize_year("Mar 2019") == "Mar 2019"

def test_year_7():
    assert normalize_year("Mar 2018") == "Mar 2018"

def test_year_8():
    assert normalize_year("Mar 2017") == "Mar 2017"

def test_year_9():
    assert normalize_year("Mar 2016") == "Mar 2016"

def test_year_10():
    assert normalize_year("Mar 2015") == "Mar 2015"

def test_year_11():
    assert normalize_year(2024) == "2024"

def test_year_12():
    assert normalize_year(2023) == "2023"

def test_year_13():
    assert normalize_year(2022) == "2022"

def test_year_14():
    assert normalize_year(2021) == "2021"

def test_year_15():
    assert normalize_year(2020) == "2020"

def test_year_16():
    assert normalize_year(2019) == "2019"

def test_year_17():
    assert normalize_year(2018) == "2018"

def test_year_18():
    assert normalize_year(2017) == "2017"

def test_year_19():
    assert normalize_year(2016) == "2016"

def test_year_20():
    assert normalize_year(2015) == "2015"