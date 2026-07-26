from src.screener.engine import run


def test_scoring():
    """Verify that the screening engine output includes composite quality scores."""

    df = run()

    assert "composite_quality_score" in df.columns
