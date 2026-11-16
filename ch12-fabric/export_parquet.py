"""Writes the five Meridian tables as Parquet files in ./upload, ready to upload to a Fabric lakehouse.

Dates are written as DATE and money as DECIMAL, the types Spark and the SQL endpoint expect.
"""
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine

PG_URL = 'postgresql+psycopg2://meridian_user:meridian2024@localhost:5432/meridian_db'
TABLES = ['dim_country', 'dim_category', 'dim_customer', 'dim_product', 'fact_orders']
MONEY = {'unit_price': pa.decimal128(8, 2), 'total_amount': pa.decimal128(10, 2)}

out = Path('upload')
out.mkdir(exist_ok=True)
pg = create_engine(PG_URL)
for table in TABLES:
    df = pd.read_sql(f'SELECT * FROM {table} ORDER BY 1', pg)
    fields = []
    for col in df.columns:
        if col in MONEY:
            df[col] = [Decimal(str(v)).quantize(Decimal('0.01'))
                       for v in df[col]]
            fields.append(pa.field(col, MONEY[col]))
        elif col.endswith('_date'):
            df[col] = pd.to_datetime(df[col]).dt.date
            fields.append(pa.field(col, pa.date32()))
        elif col.endswith('_id') or col == 'quantity':
            fields.append(pa.field(col, pa.int32()))
        else:
            fields.append(pa.field(col, pa.string()))
    arrow = pa.Table.from_pandas(df, schema=pa.schema(fields), preserve_index=False)
    path = out / f'{table}.parquet'
    pq.write_table(arrow, path)
    print(f'{path}  {arrow.num_rows:>8,} rows  {path.stat().st_size:>10,} bytes')
