"""Chapter 16, Step 4 — windows on a stream: revenue per one-minute window.

TestStream replays events with their own timestamps, so the result is the same at
every run. On a real stream (Kafka, Pub/Sub) only the first step changes.
"""
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.testing.test_stream import TestStream
from apache_beam.transforms import window

START = 1_700_000_000          # 14 November 2023, 22:13:20 UTC, in seconds
events = [                     # (seconds after START, order value)
    (5, 120.00), (20, 80.50), (55, 42.25),
    (65, 300.00), (90, 19.99),
    (130, 75.00), (170, 25.00), (179, 5.01),
]
stream = TestStream().advance_watermark_to(START)
for offset, amount in events:
    stream = stream.add_elements([window.TimestampedValue(amount, START + offset)])
stream = stream.advance_watermark_to_infinity()

options = PipelineOptions()
options.view_as(StandardOptions).streaming = True


class AddWindowStart(beam.DoFn):
    def process(self, total, win=beam.DoFn.WindowParam):
        yield f'window starting {win.start.to_utc_datetime():%H:%M:%S}  revenue {total:.2f}'


with beam.Pipeline(options=options) as p:
    (p
     | 'Events' >> stream
     | 'One-minute windows' >> beam.WindowInto(window.FixedWindows(60))
     | 'Sum per window' >> beam.CombineGlobally(sum).without_defaults()
     | 'Label' >> beam.ParDo(AddWindowStart())
     | 'Print' >> beam.Map(print))
