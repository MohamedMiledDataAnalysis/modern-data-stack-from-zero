# Chapter 13 — Apache Spark

From this folder, with PostgreSQL running and the virtual environment active:

1. `python export_lake.py` — writes the raw zone to `~/meridian/lake/raw`
2. `python spark_basics.py` — Steps 1 to 5
3. `python spark_clean.py` — Step 6: writes `~/meridian/lake/cleaned/orders`
4. `python solutions/exercises.py` — corrections to the exercises

Spark's web interface is at http://localhost:4040 while a script runs.
