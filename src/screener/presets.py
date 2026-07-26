from src.screener.engine import run

PRESETS = {
    "quality_compounder": {
        "roe_pct": 15,
        "total_debt_cr": 1,
        "cash_from_operations_cr": 0,
        "revenue_cr": 1000,
    },
    "value_pick": {"total_debt_cr": 2, "dividend_payout_ratio_pct": 1},
    "growth_accelerator": {"net_profit_margin_pct": 20, "cash_from_operations_cr": 0},
    "dividend_champion": {"dividend_payout_ratio_pct": 2, "cash_from_operations_cr": 0},
    "debt_free_bluechip": {"total_debt_cr": 0, "roe_pct": 12, "revenue_cr": 5000},
    "turnaround_watch": {"cash_from_operations_cr": 0},
}


def list_presets():
    """Return a list of all available stock screening preset names."""

    return list(PRESETS.keys())


def apply_preset(name):
    """Execute the stock screening workflow for a specified preset configuration."""

    if name not in PRESETS:
        raise ValueError(f"Unknown preset: {name}")

    print(f"Running preset: {name}")
    return run()


if __name__ == "__main__":
    for preset in list_presets():
        df = apply_preset(preset)
        print(f"{preset}: {len(df)} companies")
        print(df.head())
        print("-" * 60)
