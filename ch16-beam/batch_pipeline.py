"""Chapter 16, Step 3 — a batch pipeline: monthly completed revenue from the raw zone."""
import argparse
from pathlib import Path

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

RAW = str(Path.home() / 'meridian' / 'lake' / 'raw' / 'orders' / '*' / '*' / '*.parquet')
OUT = str(Path.home() / 'meridian' / 'lake' / 'beam' / 'monthly_revenue')

parser = argparse.ArgumentParser()
parser.add_argument('--input', default=RAW)
parser.add_argument('--output', default=OUT)
args, beam_args = parser.parse_known_args()     # the rest (--runner ...) goes to Beam

with beam.Pipeline(options=PipelineOptions(beam_args)) as p:
    (p
     | 'Read raw orders' >> beam.io.ReadFromParquet(
           args.input, columns=['order_date', 'status', 'total_amount'])
     | 'Keep completed' >> beam.Filter(lambda o: o['status'] == 'completed')
     | 'Key by month' >> beam.Map(lambda o: (o['order_date'].strftime('%Y-%m'),
                                             o['total_amount']))
     | 'Sum per month' >> beam.CombinePerKey(sum)
     | 'Format' >> beam.MapTuple(lambda month, revenue: f'{month},{revenue:.2f}')
     | 'Write' >> beam.io.WriteToText(args.output, file_name_suffix='.csv',
                                      header='month,revenue', num_shards=1))
print('Written to', args.output + '-00000-of-00001.csv')
