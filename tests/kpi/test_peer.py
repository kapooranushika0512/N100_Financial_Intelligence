from src.analytics.peer import run


def test_peer():
    """Verify peer analysis execution returns a non-empty DataFrame containing percentile ranks."""

    df = run()

    assert df is not None
    assert len(df) > 0
    assert "percentile_rank" in df.columns
