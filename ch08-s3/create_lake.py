"""Chapter 8, Step 2 — create the bucket and fill the raw zone."""
import io

import pandas as pd
from sqlalchemy import create_engine

from lake_config import BUCKET, REGION, s3_client

s3 = s3_client()
s3.create_bucket(Bucket=BUCKET, CreateBucketConfiguration={
    'LocationConstraint': REGION})
print('Bucket created:', BUCKET)

# 1. the supplier file, exactly as received
s3.upload_file('../ch02-files-apis-iot/supplier_stock.csv',
               BUCKET,
               'raw/supplier_stock/2026-09-22/supplier_stock.csv')

# 2. the orders, one Parquet file per month
URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')          # Chapter 1
orders = pd.read_sql(
    'SELECT * FROM fact_orders ORDER BY order_id',
    create_engine(URL), parse_dates=['order_date'])
for (year, month), part in orders.groupby(
        [orders.order_date.dt.year, orders.order_date.dt.month]):
    buf = io.BytesIO()
    part.to_parquet(buf, index=False)
    key = (f'raw/orders/year={year}/month={month:02d}'
           '/orders.parquet')
    s3.put_object(Bucket=BUCKET, Key=key, Body=buf.getvalue())

objects = s3.list_objects_v2(Bucket=BUCKET, Prefix='raw/orders/')
print(f"{objects['KeyCount']} order files uploaded")
print('first:', objects['Contents'][0]['Key'])
print('last: ', objects['Contents'][-1]['Key'])
print(sum(o['Size'] < 131072 for o in objects['Contents']), 'files under 128 KB')
