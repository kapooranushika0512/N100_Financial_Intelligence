import pandas as pd

files = [
    "stock_prices.xlsx",
    "sectors.xlsx",
    "peer_groups.xlsx",
    "market_cap.xlsx"
]

for file in files:
    print("\n" + "="*50)
    print(file)
    print("="*50)

    df = pd.read_excel(f"data/supporting/{file}", header=0)
    print(df.columns.tolist())
    