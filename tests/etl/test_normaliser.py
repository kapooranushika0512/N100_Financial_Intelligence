import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src" / "etl"))

from normaliser import normalize_ticker, normalize_year


def test_ticker_1():
    """Verify normalize_ticker converts lowercase ticker to uppercase."""
    assert normalize_ticker("abb") == "ABB"


def test_ticker_2():
    """Verify normalize_ticker formats TCS correctly."""
    assert normalize_ticker("tcs") == "TCS"


def test_ticker_3():
    """Verify normalize_ticker formats INFY correctly."""
    assert normalize_ticker("infy") == "INFY"


def test_ticker_4():
    """Verify normalize_ticker strips surrounding whitespace."""
    assert normalize_ticker(" hdfcbank ") == "HDFCBANK"


def test_ticker_5():
    """Verify normalize_ticker formats RELIANCE correctly."""
    assert normalize_ticker("reliance") == "RELIANCE"


def test_ticker_6():
    """Verify normalize_ticker formats SBIN correctly."""
    assert normalize_ticker("sbin") == "SBIN"


def test_ticker_7():
    """Verify normalize_ticker formats ITC correctly."""
    assert normalize_ticker("itc") == "ITC"


def test_ticker_8():
    """Verify normalize_ticker formats ASIANPAINT correctly."""
    assert normalize_ticker("asianpaint") == "ASIANPAINT"


def test_ticker_9():
    """Verify normalize_ticker formats KOTAKBANK correctly."""
    assert normalize_ticker("kotakbank") == "KOTAKBANK"


def test_ticker_10():
    """Verify normalize_ticker formats AXISBANK correctly."""
    assert normalize_ticker("axisbank") == "AXISBANK"


def test_ticker_11():
    """Verify normalize_ticker formats WIPRO correctly."""
    assert normalize_ticker("wipro") == "WIPRO"


def test_ticker_12():
    """Verify normalize_ticker formats ULTRACEMCO correctly."""
    assert normalize_ticker("ultracemco") == "ULTRACEMCO"


def test_ticker_13():
    """Verify normalize_ticker formats NESTLEIND correctly."""
    assert normalize_ticker("nestleind") == "NESTLEIND"


def test_ticker_14():
    """Verify normalize_ticker formats BAJAJAUTO correctly."""
    assert normalize_ticker("bajajauto") == "BAJAJAUTO"


def test_ticker_15():
    """Verify normalize_ticker formats SUNPHARMA correctly."""
    assert normalize_ticker("sunpharma") == "SUNPHARMA"


def test_year_1():
    """Verify normalize_year retains month-year string format for 2024."""
    assert normalize_year("Mar 2024") == "Mar 2024"


def test_year_2():
    """Verify normalize_year retains month-year string format for 2023."""
    assert normalize_year("Mar 2023") == "Mar 2023"


def test_year_3():
    """Verify normalize_year retains month-year string format for 2022."""
    assert normalize_year("Mar 2022") == "Mar 2022"


def test_year_4():
    """Verify normalize_year retains month-year string format for 2021."""
    assert normalize_year("Mar 2021") == "Mar 2021"


def test_year_5():
    """Verify normalize_year retains month-year string format for 2020."""
    assert normalize_year("Mar 2020") == "Mar 2020"


def test_year_6():
    """Verify normalize_year retains month-year string format for 2019."""
    assert normalize_year("Mar 2019") == "Mar 2019"


def test_year_7():
    """Verify normalize_year retains month-year string format for 2018."""
    assert normalize_year("Mar 2018") == "Mar 2018"


def test_year_8():
    """Verify normalize_year retains month-year string format for 2017."""
    assert normalize_year("Mar 2017") == "Mar 2017"


def test_year_9():
    """Verify normalize_year retains month-year string format for 2016."""
    assert normalize_year("Mar 2016") == "Mar 2016"


def test_year_10():
    """Verify normalize_year retains month-year string format for 2015."""
    assert normalize_year("Mar 2015") == "Mar 2015"


def test_year_11():
    """Verify normalize_year converts integer 2024 to string."""
    assert normalize_year(2024) == "2024"


def test_year_12():
    """Verify normalize_year converts integer 2023 to string."""
    assert normalize_year(2023) == "2023"


def test_year_13():
    """Verify normalize_year converts integer 2022 to string."""
    assert normalize_year(2022) == "2022"


def test_year_14():
    """Verify normalize_year converts integer 2021 to string."""
    assert normalize_year(2021) == "2021"


def test_year_15():
    """Verify normalize_year converts integer 2020 to string."""
    assert normalize_year(2020) == "2020"


def test_year_16():
    """Verify normalize_year converts integer 2019 to string."""
    assert normalize_year(2019) == "2019"


def test_year_17():
    """Verify normalize_year converts integer 2018 to string."""
    assert normalize_year(2018) == "2018"


def test_year_18():
    """Verify normalize_year converts integer 2017 to string."""
    assert normalize_year(2017) == "2017"


def test_year_19():
    """Verify normalize_year converts integer 2016 to string."""
    assert normalize_year(2016) == "2016"


def test_year_20():
    """Verify normalize_year converts integer 2015 to string."""
    assert normalize_year(2015) == "2015"
