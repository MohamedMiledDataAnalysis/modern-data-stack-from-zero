"""Chapter 2, Step 2 — the same file with pandas."""
import pandas as pd

df = pd.read_csv('supplier_stock.csv')
print(df.dtypes)

df['stock_qty'] = pd.to_numeric(df['stock_qty'], errors='coerce')
df['updated'] = pd.to_datetime(df['updated'], format='%Y-%m-%d', errors='coerce')
invalid = df[df['stock_qty'].isna() | df['updated'].isna()
             | ~df['product_id'].between(1, 500)]
print(f'{len(invalid)} invalid rows')
print(f"{(df['stock_qty'] < df['reorder_level']).sum()} products below reorder level")
