# Chapter 11 — BigQuery

Real BigQuery (the free sandbox):

```bash
gcloud auth application-default login
export MERIDIAN_BQ_MODE=gcp MERIDIAN_GCP_PROJECT=<your-project-id>
python load_bigquery.py
python query_bigquery.py
python solutions/exercises.py
```

Partitioning is off by default: in the sandbox, partitions older than 60 days expire at once. With billing enabled, `export MERIDIAN_BQ_PARTITION=1`.

The workflow tests the load and queries on the BigQuery emulator 0.8.1 with the first quarter of 2023. `check_exercises.sql` gives the exercise answers in PostgreSQL.
