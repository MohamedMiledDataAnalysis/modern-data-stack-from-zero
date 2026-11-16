"""Chapter 9, Step 2 — create the bucket and fill the raw zone on Cloud Storage."""
import io

import pandas as pd
from sqlalchemy import create_engine

from lake_config import BUCKET, LOCATION, gcs_client

client = gcs_client()
bucket = client.create_bucket(BUCKET, location=LOCATION)
print('Bucket created:', bucket.name, 'in', bucket.location)

bucket.blob('raw/supplier_stock/2026-09-22/supplier_stock.csv').upload_from_filename(
    '../ch02-files-apis-iot/supplier_stock.csv')

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
orders = pd.read_sql('SELECT * FROM fact_orders ORDER BY order_id', create_engine(URL),
                     parse_dates=['order_date'])
for (year, month), part in orders.groupby([orders.order_date.dt.year,
                                           orders.order_date.dt.month]):
    buf = io.BytesIO()
    part.to_parquet(buf, index=False)
    name = f'raw/orders/year={year}/month={month:02d}/orders.parquet'
    bucket.blob(name).upload_from_string(buf.getvalue(),
                                         content_type='application/octet-stream')

blobs = list(client.list_blobs(BUCKET, prefix='raw/orders/'))
print(f'{len(blobs)} order files uploaded')
print('first:', blobs[0].name)
print('last: ', blobs[-1].name)
