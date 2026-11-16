"""Writes orders_flat.csv, the flat table of orders_flat.sql, for Data Studio's (formerly Looker Studio's) CSV file upload."""
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

PG_URL = 'postgresql+psycopg2://meridian_user:meridian2024@localhost:5432/meridian_db'
sql = Path('orders_flat.sql').read_text()
with create_engine(PG_URL).connect() as conn:
    df = pd.read_sql(text(sql), conn)
df = df.sort_values('order_id')                 # the same row order on every machine
df.to_csv('orders_flat.csv', index=False)
size = Path('orders_flat.csv').stat().st_size
print(f'orders_flat.csv: {len(df):,} rows, {size / 1e6:.1f} MB')
print(df.head(3)[['order_id', 'order_date', 'status', 'total_amount', 'country_name']]
      .to_string(index=False))
