import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src" / "etl"))

from normaliser import normalize_ticker, normalize_year


def test_normalize_ticker():
    assert normalize_ticker("abb") == "ABB"


def test_normalize_ticker_spaces():
    assert normalize_ticker(" tcs ") == "TCS"


def test_normalize_year():
    assert normalize_year("Mar 2024") == "Mar 2024"


def test_normalize_year_number():
    assert normalize_year(2024) == "2024"