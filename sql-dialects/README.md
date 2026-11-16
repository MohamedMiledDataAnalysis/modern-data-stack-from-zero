# SQL: one language, many dialects

The same five questions about Meridian, written in the five dialects the book uses.
Every version returns the same answers (see the interlude after Chapter 1), with one exception on the BigQuery emulator: query 4's running total comes back as 0. That is a fault of the emulator; real BigQuery returns 3090147.46, 5850606.69 and 8841165.89.

| File | Dialect | Run it with |
|:--|:--|:--|
| `postgresql.sql` | PostgreSQL (Chapter 1) | `psql -h localhost -U meridian_user meridian_db -f postgresql.sql` |
| `snowflake.sql` | Snowflake SQL (Chapter 10) | `python run_snowflake.py`, in Chapter 10's environment, after `load_snowflake.py` |
| `bigquery.sql` | GoogleSQL (Chapter 11) | `python run_bigquery.py`, after Chapter 11's `load_bigquery.py` |
| `tsql.sql` | T-SQL (Chapter 12) | the Fabric SQL endpoint, or `python ../ch12-fabric/tsql/run_sql.py tsql.sql` on SQL Server, after `python tsql/load_sqlserver.py` run from `ch12-fabric/` |
| `sparksql.sql` | Spark SQL (Chapters 13, 15) | `python run_spark.py` |
