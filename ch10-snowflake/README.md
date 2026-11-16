# Chapter 10 — Snowflake

Local mode (default) uses fakesnow, which imitates Snowflake on DuckDB:

```bash
python load_snowflake.py
python query_snowflake.py
python solutions/exercises.py
```

Real Snowflake: `export MERIDIAN_SF_MODE=snowflake` and set `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, and `SNOWFLAKE_PASSWORD` or `SNOWFLAKE_PRIVATE_KEY_FILE`.

The connector is pinned to 4.8.1: fakesnow 0.12.1 does not work with connector 5.
