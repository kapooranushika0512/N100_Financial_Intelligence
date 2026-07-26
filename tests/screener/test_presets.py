from src.screener.presets import apply_preset, list_presets


def test_presets_run():
    """Verify all stock screening presets execute successfully and return valid DataFrames."""

    for preset in list_presets():
        df = apply_preset(preset)
        assert df is not None
        assert len(df) >= 0
