from src.screener.engine import run


def test_scoring():

    df = run()

    assert "composite_quality_score" in df.columns