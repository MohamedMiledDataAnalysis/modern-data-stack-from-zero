"""Chapter 2, Step 8 - read purchase orders from SQL Server and load them into PostgreSQL.

The platform connects with the read-only login meridian_reader: it can read the
purchasing database but cannot change it.
"""
import pandas as pd
from sqlalchemy import create_engine, text

SQLSERVER = 'mssql+pymssql://meridian_reader:Reader2026!@localhost:1433/meridian_erp'
POSTGRES = 'postgresql+psycopg2://meridian_user:meridian2024@localhost:5432/meridian_db'

source = create_engine(SQLSERVER)
with source.connect() as conn:
    print(conn.execute(text('SELECT @@VERSION')).scalar().splitlines()[0])
    orders = pd.read_sql(text('SELECT * FROM dbo.purchase_orders ORDER BY po_id'), conn)

print(orders.shape)
print(orders.groupby('status').size().to_string())

received = orders[orders['status'] == 'received'].copy()
received['cost'] = received['quantity'] * received['unit_cost'].astype(float)
print(received.groupby('supplier')['cost'].sum().round(2).to_string())

orders.to_sql('purchase_orders', create_engine(POSTGRES), if_exists='replace', index=False)
print(f'{len(orders)} rows written to purchase_orders in PostgreSQL')
