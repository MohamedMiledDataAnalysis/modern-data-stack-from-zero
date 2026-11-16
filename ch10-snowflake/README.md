# Chapter 10 — Snowflake

This chapter runs in its own environment (the connector's pandas tools need pandas 2):

```bash
cd ~/meridian
python3.13 -m venv snowflake-venv
source snowflake-venv/bin/activate      # Windows: snowflake-venv\Scripts\Activate.ps1
pip install -r modern-data-stack-from-zero/ch10-snowflake/requirements.txt
```

Local mode (default) uses fakesnow, which imitates Snowflake on DuckDB:

```bash
python load_snowflake.py
python query_snowflake.py
python solutions/exercises.py
```

Real Snowflake: `export MERIDIAN_SF_MODE=snowflake` and set `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, and `SNOWFLAKE_PASSWORD` or `SNOWFLAKE_PRIVATE_KEY_FILE`.

The connector is pinned to 4.8.1: fakesnow 0.12.1 does not work with connector 5.
