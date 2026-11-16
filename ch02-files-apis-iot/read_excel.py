"""Chapter 2, Step 3 — read both sheets of the supplier workbook."""
import pandas as pd

sheets = pd.read_excel('supplier_prices.xlsx', sheet_name=None)
for name, df in sheets.items():
    print(f'Sheet {name!r}: {len(df)} rows, '
          f'columns {list(df.columns)}')

prices = sheets['Prices']
print(prices.head(3))
mean_price = round(prices['supplier_price_gbp'].mean(), 2)
print('Mean supplier price:', mean_price)
