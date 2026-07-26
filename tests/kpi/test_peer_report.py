from pathlib import Path

from src.analytics.peer_report import run


def test_peer_report():
    """Verify that peer comparison report generation creates the output Excel file."""

    run(limit=1)

    assert Path("output/peer_comparison.xlsx").exists()
