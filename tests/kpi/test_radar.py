from src.analytics.radar import run
import os


def test_radar():

    run(limit=1)

    assert os.path.isdir(
        "reports/radar_charts"
    )

    files = os.listdir(
        "reports/radar_charts"
    )

    assert len(files) >= 1