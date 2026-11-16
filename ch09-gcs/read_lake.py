"""Chapter 9, Step 3 — read one month back from Cloud Storage."""
import io

import pandas as pd

from lake_config import BUCKET, gcs_client

key = 'raw/orders/year=2023/month=09/orders.parquet'
blob = gcs_client().bucket(BUCKET).blob(key)
data = blob.download_as_bytes()
print(f'{blob.name}: {len(data):,} bytes')
sept = pd.read_parquet(io.BytesIO(data))
done = sept[sept.status == 'completed']
print(f'{len(sept)} orders, {len(done)} completed, '
      f'revenue {done.total_amount.sum():,.2f}')
