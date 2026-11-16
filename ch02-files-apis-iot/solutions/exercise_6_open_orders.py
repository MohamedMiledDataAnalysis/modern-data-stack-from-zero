"""Chapter 2, Exercise 6 - which supplier has the most open purchase orders?

The query runs inside SQL Server, in its own dialect (T-SQL): TOP instead of LIMIT.
"""
from sqlalchemy import create_engine, text

SQLSERVER = 'mssql+pymssql://meridian_reader:Reader2026!@localhost:1433/meridian_erp'

query = text('''
    SELECT TOP 1 supplier, COUNT(*) AS open_orders
    FROM dbo.purchase_orders
    WHERE status = 'open'
    GROUP BY supplier
    ORDER BY open_orders DESC''')
with create_engine(SQLSERVER).connect() as conn:
    supplier, n = conn.execute(query).one()
print(f'{supplier}: {n} open purchase orders')
