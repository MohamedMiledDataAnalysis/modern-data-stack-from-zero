"""Optional: loads the Parquet files of ./upload into a local SQL Server, to practise the T-SQL
of Chapter 12 without a Fabric account. Start SQL Server first (see the README)."""
import pandas as pd
from sqlalchemy import create_engine, text

URL = 'mssql+pymssql://sa:Meridian2026!@localhost:1433/master'
TABLES = ['dim_country', 'dim_category', 'dim_customer', 'dim_product', 'fact_orders']

engine = create_engine(URL, isolation_level='AUTOCOMMIT')
with engine.connect() as conn:
    conn.execute(text("IF DB_ID('meridian') IS NULL CREATE DATABASE meridian"))
engine = create_engine(URL.replace('/master', '/meridian'))
for table in TABLES:
    df = pd.read_parquet(f'upload/{table}.parquet')
    df.to_sql(table, engine, schema='dbo', if_exists='replace', index=False,
              chunksize=200, method='multi')
    print(f'{table:<13}{len(df):>8,} rows')
