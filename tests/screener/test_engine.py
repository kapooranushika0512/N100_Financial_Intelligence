from src.screener.engine import run


def test_engine_runs():
    """Verify stock screening engine executes successfully and returns non-empty results."""

    df = run()

    assert df is not None
    assert len(df) > 0
