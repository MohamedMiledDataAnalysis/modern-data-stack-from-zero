"""Make Meridian's orders larger, to see how tools behave as data grows.

The Modern Data Stack, Second Edition, Chapter 17, Step 7.
Needs the cleaned zone of Chapter 13 (~/meridian/lake/cleaned/orders).

    python scale_up.py --factor 20

writes 20 copies of the 250,000 cleaned orders, 5,000,000 rows, to
~/meridian/lake/scaled/orders/, one Parquet file per copy. Copy k adds
k * 1,000,000 to every order_id, so every order_id stays unique. Every other
value is unchanged: any total on the scaled data is exactly `factor` times
the same total on the original data.

The script holds one copy in memory at a time, so it runs on any machine.
"""
import argparse
import shutil
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.parquet as pq

LAKE = Path.home() / 'meridian' / 'lake'

parser = argparse.ArgumentParser()
parser.add_argument('--factor', type=int, default=20)
args = parser.parse_args()

source = ds.dataset(LAKE / 'cleaned' / 'orders', format='parquet',
                    partitioning='hive').to_table()
source = source.drop_columns(['cleaned_at'])
# Spark wrote the cleaned zone, and stored its own copy of the schema in the file;
# drop it, or Spark would read the old columns back from it
source = source.replace_schema_metadata(None)
source = source.set_column(source.schema.get_field_index('year'), 'year',
                           pc.cast(source['year'], pa.int32()))
source = source.set_column(source.schema.get_field_index('month'), 'month',
                           pc.cast(source['month'], pa.int32()))

target = LAKE / 'scaled' / 'orders'
shutil.rmtree(target, ignore_errors=True)
target.mkdir(parents=True)

for k in range(args.factor):
    ids = pc.add(source['order_id'], k * 1_000_000)
    copy = source.set_column(0, 'order_id', ids)
    pq.write_table(copy, target / f'part-{k:03d}.parquet')

size = sum(f.stat().st_size for f in target.iterdir()) / 1e6
print(f'{args.factor * source.num_rows:,} orders written to {target}')
print(f'{size:,.0f} MB on disk, in {args.factor} Parquet files')
