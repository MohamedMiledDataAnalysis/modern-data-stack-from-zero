"""Chapter 2, Exercise 6 - how many open purchase orders does each supplier have?

The query runs inside SQL Server, in its own dialect (T-SQL). Baltic Goods and
Northwind tie with 132 open orders each: the second sort key, supplier, fixes the
order of the tied rows. To keep only the leaders, T-SQL writes SELECT TOP 1 WITH TIES.
"""
from sqlalchemy import create_engine, text

SQLSERVER = ('mssql+pymssql://meridian_reader:Reader2026!'
             '@localhost:1433/meridian_erp')

query = text('''
    SELECT supplier, COUNT(*) AS open_orders
    FROM dbo.purchase_orders
    WHERE status = 'open'
    GROUP BY supplier
    ORDER BY open_orders DESC, supplier''')
with create_engine(SQLSERVER).connect() as conn:
    for supplier, n in conn.execute(query):
        print(f'{supplier}: {n} open purchase orders')
