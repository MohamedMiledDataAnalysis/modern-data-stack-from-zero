"""Chapter 13, Step 0 — write the raw zone to your disk, in the layout of Chapter 8.

Spark reads it from ~/meridian/lake. (Reading straight from S3 needs extra
Java libraries; Chapter 15 does it on Databricks.)
"""
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

LAKE = Path.home() / 'meridian' / 'lake'
URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)

orders = pd.read_sql('SELECT * FROM fact_orders ORDER BY order_id', engine, parse_dates=['order_date'])
for (year, month), part in orders.groupby([orders.order_date.dt.year,
                                           orders.order_date.dt.month]):
    folder = LAKE / 'raw' / 'orders' / f'year={year}' / f'month={month:02d}'
    folder.mkdir(parents=True, exist_ok=True)
    part.to_parquet(folder / 'orders.parquet', index=False)

for table in ['dim_customer', 'dim_product', 'dim_country', 'dim_category']:
    folder = LAKE / 'raw' / table
    folder.mkdir(parents=True, exist_ok=True)
    pd.read_sql(f'SELECT * FROM {table} ORDER BY 1', engine).to_parquet(folder / f'{table}.parquet',
                                                            index=False)
print('Raw zone written to', LAKE / 'raw')
