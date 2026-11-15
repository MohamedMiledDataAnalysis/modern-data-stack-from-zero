"""Chapter 2, Step 7 — load the valid supplier rows into PostgreSQL."""
import pandas as pd
from sqlalchemy import create_engine

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')

df = pd.read_csv('supplier_stock.csv')
df['stock_qty'] = pd.to_numeric(df['stock_qty'], errors='coerce')
df['updated'] = pd.to_datetime(df['updated'], format='%Y-%m-%d', errors='coerce')
valid = df.dropna(subset=['stock_qty', 'updated'])
valid = valid[valid['product_id'].between(1, 500)]
valid = valid.astype({'stock_qty': 'int64'})

engine = create_engine(URL)
valid.to_sql('supplier_stock', engine, if_exists='replace', index=False)
print(f'{len(valid)} rows written to supplier_stock')
