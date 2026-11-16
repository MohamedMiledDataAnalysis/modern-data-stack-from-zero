"""Chapter 2, Step 8 - create Meridian's purchasing database in SQL Server.

Meridian's purchasing team runs its own application on SQL Server: every order
sent to a supplier is a row in dbo.purchase_orders. This script plays that
application. It creates the database meridian_erp, the table, 2,000 purchase
orders (seed 11: every reader gets the same rows) and a read-only login,
meridian_reader, for the data platform.
"""
import random
from datetime import date, timedelta

import pymssql

SA = dict(server='localhost', port=1433, user='sa', password='Meridian2026!')
SUPPLIERS = ['Northwind', 'Alder & Co', 'Baltic Goods']
STATUSES = ['received', 'received', 'received', 'open', 'cancelled']

random.seed(11)
rows = []
for po_id in range(1, 2001):
    order_date = date(2023, 1, 1) + timedelta(days=random.randint(0, 364))
    rows.append((po_id, random.choice(SUPPLIERS), random.randint(1, 500),
                 order_date, random.randint(1, 20) * 10,
                 round(random.uniform(1.5, 300), 2), random.choice(STATUSES)))

conn = pymssql.connect(**SA, autocommit=True)
cur = conn.cursor()
cur.execute("IF DB_ID('meridian_erp') IS NOT NULL "
            "BEGIN ALTER DATABASE meridian_erp SET SINGLE_USER WITH ROLLBACK IMMEDIATE; "
            "DROP DATABASE meridian_erp; END")
cur.execute('CREATE DATABASE meridian_erp')
cur.execute('USE meridian_erp')
cur.execute('''CREATE TABLE dbo.purchase_orders (
    po_id      INT           PRIMARY KEY,
    supplier   NVARCHAR(50)  NOT NULL,
    product_id INT           NOT NULL,
    order_date DATE          NOT NULL,
    quantity   INT           NOT NULL,
    unit_cost  DECIMAL(8,2)  NOT NULL,
    status     NVARCHAR(20)  NOT NULL)''')
cur.executemany('INSERT INTO dbo.purchase_orders VALUES (%d, %s, %d, %s, %d, %s, %s)', rows)
cur.execute("IF SUSER_ID('meridian_reader') IS NULL "
            "CREATE LOGIN meridian_reader WITH PASSWORD = 'Reader2026!'")
cur.execute('CREATE USER meridian_reader FOR LOGIN meridian_reader')
cur.execute("ALTER ROLE db_datareader ADD MEMBER meridian_reader")
cur.execute('SELECT COUNT(*) FROM dbo.purchase_orders')
print(cur.fetchone()[0], 'purchase orders written to meridian_erp.dbo.purchase_orders')
conn.close()
