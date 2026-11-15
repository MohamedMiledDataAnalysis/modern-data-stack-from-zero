"""Chapter 8 — corrections to Exercises 1 to 4.

Run from the ch08-s3 folder, after create_lake.py and lifecycle.py:
    python solutions/exercises.py
"""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from lake_config import BUCKET, s3_client

s3 = s3_client()

# Exercise 1
total, n = 0, 0
for page in s3.get_paginator('list_objects_v2').paginate(
        Bucket=BUCKET, Prefix='raw/orders/year=2022/'):
    for obj in page['Contents']:
        total += obj['Size']
        n += 1
print('Exercise 1:', n, total)

# Exercise 2
frames = [pd.read_parquet(io.BytesIO(s3.get_object(
    Bucket=BUCKET, Key=f'raw/orders/year=2022/month={m:02d}/orders.parquet')['Body'].read()))
    for m in range(1, 13)]
df = pd.concat(frames)
print('Exercise 2:', len(df), len(df.to_csv(index=False).encode()))

# Exercise 3
s3.upload_file('../ch02-files-apis-iot/supplier_stock.csv', BUCKET,
               'raw/supplier_stock/2026-09-22/supplier_stock.csv')
v = s3.list_object_versions(Bucket=BUCKET, Prefix='raw/supplier_stock/')
print('Exercise 3:', len(v['Versions']), [x['IsLatest'] for x in v['Versions']])

# Exercise 4
print('Exercise 4:', round(df.loc[df.status == 'completed', 'total_amount'].sum(), 2))
