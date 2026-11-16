"""Creates the five Meridian tables in Snowflake, then copies their rows from PostgreSQL."""
from sf_config import MODE, PG_URL, TABLES, sf_connect   # first: sets up local mode

import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from sqlalchemy import create_engine

pg = create_engine(PG_URL)
conn = sf_connect()
print('mode:', MODE)
conn.execute_string(open('create_tables.sql').read())   # runs each statement in turn
for table in TABLES:
    df = pd.read_sql(f'SELECT * FROM {table}', pg)
    df.columns = [c.upper() for c in df.columns]       # Snowflake's default case
    ok, chunks, rows, _ = write_pandas(conn, df, table.upper())
    print(f'{table:<13}{rows:>8,} rows  ok={ok}')
conn.close()
