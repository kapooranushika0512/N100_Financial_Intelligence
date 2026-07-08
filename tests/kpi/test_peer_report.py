from pathlib import Path

from src.analytics.peer_report import run


def test_peer_report():

    run(limit=1)

    assert Path("output/peer_comparison.xlsx").exists()