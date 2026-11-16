"""Chapter 8, Step 4 — read one month back from the lake."""
import io

import pandas as pd

from lake_config import BUCKET, s3_client

s3 = s3_client()
key = 'raw/orders/year=2023/month=09/orders.parquet'
head = s3.head_object(Bucket=BUCKET, Key=key)
print(f"{key}: {head['ContentLength']:,} bytes")

body = s3.get_object(Bucket=BUCKET, Key=key)['Body'].read()
sept = pd.read_parquet(io.BytesIO(body))
print(sept.dtypes)
done = sept[sept.status == 'completed']
print(f'{len(sept)} orders, {len(done)} completed, '
      f'revenue {done.total_amount.sum():,.2f}')
