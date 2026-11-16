"""Runs bigquery.sql on BigQuery (or the emulator), one query at a time.
    python run_bigquery.py          all five
    python run_bigquery.py 3        query 3 only
Uses Chapter 11's bq_config.py: set MERIDIAN_BQ_MODE and MERIDIAN_GCP_PROJECT as in Chapter 11."""
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, '..', 'ch11-bigquery'))
from bq_config import PROJECT, bq_client             # noqa: E402

sys.path.insert(0, here)
from statements import statements                    # noqa: E402

client = bq_client()
queries = list(statements(os.path.join(here, 'bigquery.sql')))
chosen = [int(a) for a in sys.argv[1:]] or range(1, len(queries) + 1)
for n in chosen:
    rows = client.query(queries[n - 1].replace('PROJECT', PROJECT)).result()
    print(f'-- query {n}')
    for row in rows:
        print(tuple(row.values()))
