import pandas as pd

files = [
    "financial_ratios",
    "stock_prices",
    "sectors",
    "peer_groups",
    "market_cap"
]

for file in files:

    print("\n" + "="*60)
    print(file.upper())
    print("="*60)

    df = pd.read_excel(
        f"data/supporting/{file}.xlsx",
        header=None
    )

    print(df.head(10))