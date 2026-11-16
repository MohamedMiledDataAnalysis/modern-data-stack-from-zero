"""Chapter 9, Step 4 — read one month back from Cloud Storage."""
import io

import pandas as pd

from lake_config import BUCKET, gcs_client

blob = gcs_client().bucket(BUCKET).blob('raw/orders/year=2023/month=09/orders.parquet')
data = blob.download_as_bytes()
print(f'{blob.name}: {len(data):,} bytes')
sept = pd.read_parquet(io.BytesIO(data))
done = sept[sept.status == 'completed']
print(f'{len(sept)} orders, {len(done)} completed, revenue {done.total_amount.sum():,.2f}')
