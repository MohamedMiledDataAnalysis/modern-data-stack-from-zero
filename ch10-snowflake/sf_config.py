"""Where the Chapter 10 scripts connect.

MERIDIAN_SF_MODE=local (default): fakesnow, a local imitation of Snowflake built on DuckDB.
MERIDIAN_SF_MODE=snowflake: your Snowflake account, from the SNOWFLAKE_* variables.
"""
import os

import snowflake.connector

MODE = os.environ.get('MERIDIAN_SF_MODE', 'local')
PG_URL = 'postgresql+psycopg2://meridian_user:meridian2024@localhost:5432/meridian_db'
TABLES = ['dim_country', 'dim_category', 'dim_customer', 'dim_product', 'fact_orders']

if MODE == 'local':
    import warnings

    import fakesnow
    # fakesnow 0.12.1 prints a performance notice on every query
    warnings.filterwarnings(
        'ignore', message='Arrow output on a DB-API result')
    os.makedirs('fakesnow_data', exist_ok=True)
    # keep the tables in fakesnow_data/ between runs
    _fake = fakesnow.patch(db_path='fakesnow_data')
    _fake.__enter__()            # active until the script ends


def sf_connect():
    if MODE == 'local':
        conn = snowflake.connector.connect(database='MERIDIAN',
                                           schema='RAW')
        conn.cursor().execute(
            'CREATE SCHEMA IF NOT EXISTS MERIDIAN.RAW')
        return conn
    key = os.environ.get('SNOWFLAKE_PRIVATE_KEY_FILE')
    secret = ({'private_key_file': key} if key
              else {'password': os.environ['SNOWFLAKE_PASSWORD']})
    return snowflake.connector.connect(
        account=os.environ['SNOWFLAKE_ACCOUNT'],
        user=os.environ['SNOWFLAKE_USER'],
        role='SYSADMIN', warehouse='MERIDIAN_WH',
        database='MERIDIAN', schema='RAW', **secret)
