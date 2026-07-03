from src.screener.engine import run


def test_engine_runs():

    df = run()

    assert df is not None
    assert len(df) > 0