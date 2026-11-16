"""Optional: loads the Parquet files of ./upload into a local SQL Server, to practise the T-SQL
of Chapter 12 without a Fabric account. Start the sqlserver container of Chapter 2, Step 8 first
(docker start sqlserver; see the README), and run export_parquet.py from ch12-fabric/."""
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import DECIMAL, Date, Integer, String, create_engine, text

URL = 'mssql+pymssql://sa:Meridian2026!@localhost:1433/master'
TABLES = ['dim_country', 'dim_category', 'dim_customer', 'dim_product', 'fact_orders']

engine = create_engine(URL, isolation_level='AUTOCOMMIT')
with engine.connect() as conn:
    conn.execute(text("IF DB_ID('meridian') IS NULL CREATE DATABASE meridian"))
engine = create_engine(URL.replace('/master', '/meridian'))
for table in TABLES:
    path = f'upload/{table}.parquet'
    df = pd.read_parquet(path)
    types = {}                                   # SQL Server types from the Parquet types
    for field in pq.read_schema(path):
        kind = str(field.type)
        if kind.startswith('decimal'):
            types[field.name] = DECIMAL(field.type.precision, field.type.scale)
        elif kind.startswith('date'):
            types[field.name] = Date()
        elif kind.startswith('int'):
            types[field.name] = Integer()
        else:
            types[field.name] = String(100)
    df.to_sql(table, engine, schema='dbo', if_exists='replace', index=False,
              dtype=types, chunksize=200, method='multi')
    print(f'{table:<13}{len(df):>8,} rows')
