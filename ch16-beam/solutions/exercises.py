"""Chapter 16 — corrections (run in the Beam environment, after Chapter 13's export)."""
from pathlib import Path

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.testing.test_stream import TestStream
from apache_beam.transforms import window

RAW = str(Path.home() / 'meridian' / 'lake' / 'raw' / 'orders' / '*' / '*' / '*.parquet')

print('Exercise 1 — orders per status')
with beam.Pipeline() as p:
    (p | beam.io.ReadFromParquet(RAW, columns=['status'])
       | beam.Map(lambda o: o['status'])
       | beam.combiners.Count.PerElement()
       | beam.Map(print))


class SplitLarge(beam.DoFn):
    """Send completed orders above £2,000 to a second output called 'large'."""
    def process(self, order):
        if order['total_amount'] > 2000:
            yield beam.pvalue.TaggedOutput('large', order)
        else:
            yield order


print('Exercise 2 — large completed orders')
with beam.Pipeline() as p:
    parts = (p | beam.io.ReadFromParquet(RAW, columns=['status', 'total_amount'])
               | beam.Filter(lambda o: o['status'] == 'completed')
               | beam.ParDo(SplitLarge()).with_outputs('large', main='normal'))
    parts.large | 'Count large' >> beam.combiners.Count.Globally() \
                | 'Print large' >> beam.Map(lambda n: print('large:', n))
    parts.normal | 'Count normal' >> beam.combiners.Count.Globally() \
                 | 'Print normal' >> beam.Map(lambda n: print('normal:', n))

print('Exercise 3 — two-minute windows, every minute')
START = 1_700_000_000
events = [(5, 120.00), (20, 80.50), (55, 42.25), (65, 300.00), (90, 19.99),
          (130, 75.00), (170, 25.00), (179, 5.01)]
stream = TestStream().advance_watermark_to(START)
for offset, amount in events:
    stream = stream.add_elements([window.TimestampedValue(amount, START + offset)])
stream = stream.advance_watermark_to_infinity()
options = PipelineOptions()
options.view_as(StandardOptions).streaming = True


class Label(beam.DoFn):
    def process(self, total, win=beam.DoFn.WindowParam):
        yield (f'{win.start.to_utc_datetime():%H:%M}-{win.end.to_utc_datetime():%H:%M}'
               f'  revenue {total:.2f}')


with beam.Pipeline(options=options) as p:
    (p | stream
       | beam.WindowInto(window.SlidingWindows(size=120, period=60))
       | beam.CombineGlobally(sum).without_defaults()
       | beam.ParDo(Label())
       | beam.Map(print))
