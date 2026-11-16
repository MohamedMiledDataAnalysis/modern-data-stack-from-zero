"""Chapter 9 — corrections (run from the ch09-gcs folder, after create_lake.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lake_config import BUCKET, gcs_client   # noqa: E402

client = gcs_client()

print('Exercise 1 — files and bytes for 2022')
blobs = list(client.list_blobs(BUCKET, prefix='raw/orders/year=2022/'))
print(len(blobs), sum(b.size for b in blobs))

print('Exercise 2 — "folders" under raw/orders/')
it = client.list_blobs(BUCKET, prefix='raw/orders/', delimiter='/')
list(it)                      # the prefixes are filled once the pages are read
print(sorted(it.prefixes))

print('Exercise 3 — metadata on an object')
blob = client.bucket(BUCKET).blob('raw/supplier_stock/2026-09-22/supplier_stock.csv')
blob.metadata = {'supplier_batch': '2026-09-22', 'received_by': 'nifi'}
blob.patch()
blob.reload()
print(blob.metadata, blob.content_type)
