"""Chapter 16, Steps 1-4 — a batch pipeline: monthly completed revenue from the raw zone."""
from pathlib import Path

import apache_beam as beam

RAW = str(Path.home() / 'meridian' / 'lake' / 'raw' / 'orders' / '*' / '*' / '*.parquet')
OUT = str(Path.home() / 'meridian' / 'lake' / 'beam' / 'monthly_revenue')

with beam.Pipeline() as p:
    (p
     | 'Read raw orders' >> beam.io.ReadFromParquet(RAW, columns=['order_date', 'status',
                                                                  'total_amount'])
     | 'Keep completed' >> beam.Filter(lambda o: o['status'] == 'completed')
     | 'Key by month' >> beam.Map(lambda o: (o['order_date'].strftime('%Y-%m'),
                                             o['total_amount']))
     | 'Sum per month' >> beam.CombinePerKey(sum)
     | 'Format' >> beam.MapTuple(lambda month, revenue: f'{month},{revenue:.2f}')
     | 'Write' >> beam.io.WriteToText(OUT, file_name_suffix='.csv',
                                      header='month,revenue', num_shards=1))
print('Written to', OUT + '-00000-of-00001.csv')
