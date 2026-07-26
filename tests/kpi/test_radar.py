import os

from src.analytics.radar import run


def test_radar():
    """Verify radar chart generation runs successfully and outputs image files."""

    run(limit=1)

    assert os.path.isdir("reports/radar_charts")

    files = os.listdir("reports/radar_charts")

    assert len(files) >= 1
