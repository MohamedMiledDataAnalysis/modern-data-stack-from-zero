# Chapter 15 — Databricks and Delta Lake

Part A runs on your laptop, after Chapter 13 (the cleaned zone must exist):

- `python delta_local.py` — Delta table, MERGE, history, time travel, schema enforcement
- `python solutions/exercises.py` — corrections (the last one restores version 0)

The first run downloads Delta's Java libraries from Maven Central.

Part B (Databricks Free Edition):

- `python export_for_databricks.py` — gathers the 37 raw order files into one file,
  `~/meridian/lake/databricks/orders_all.parquet`, to upload to a volume
