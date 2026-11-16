"""Chapter 15, Part B — gather the 37 monthly order files into one file to upload.

Databricks' upload page takes files, not folders, and the 37 raw files all share
the name orders.parquet. One file of 250,000 orders avoids both problems.
"""
from pathlib import Path

import pandas as pd

LAKE = Path.home() / 'meridian' / 'lake'
orders = pd.read_parquet(LAKE / 'raw' / 'orders')       # reads every year=/month= folder
orders['year'] = orders['year'].astype('int32')          # folder names become columns
orders['month'] = orders['month'].astype('int32')
target = LAKE / 'databricks' / 'orders_all.parquet'
target.parent.mkdir(parents=True, exist_ok=True)
orders.to_parquet(target, index=False)
print(len(orders), 'orders written to', target)
