"""Builds meridian.hyper, a Tableau extract of the orders joined to their customer,
country, product and category, using Tableau's Hyper API."""
from pathlib import Path

from sqlalchemy import create_engine, text
from tableauhyperapi import (Connection, CreateMode, HyperProcess, Inserter, NOT_NULLABLE,
                             SqlType, TableDefinition, TableName, Telemetry)

PG_URL = 'postgresql+psycopg2://meridian_user:meridian2024@localhost:5432/meridian_db'
SQL = """
SELECT o.order_id, o.order_date, o.status, o.quantity, o.total_amount,
       cu.customer_id, cu.signup_date, c.country_name,
       p.product_name, cat.category_name
FROM fact_orders o
JOIN dim_customer cu ON cu.customer_id = o.customer_id
JOIN dim_country  c  ON c.country_id   = cu.country_id
JOIN dim_product  p  ON p.product_id   = o.product_id
JOIN dim_category cat ON cat.category_id = p.category_id
"""
ORDERS = TableDefinition(TableName('Extract', 'orders'), [
    TableDefinition.Column('order_id', SqlType.int(), NOT_NULLABLE),
    TableDefinition.Column('order_date', SqlType.date(), NOT_NULLABLE),
    TableDefinition.Column('status', SqlType.text(), NOT_NULLABLE),
    TableDefinition.Column('quantity', SqlType.int(), NOT_NULLABLE),
    TableDefinition.Column('total_amount', SqlType.numeric(10, 2), NOT_NULLABLE),
    TableDefinition.Column('customer_id', SqlType.int(), NOT_NULLABLE),
    TableDefinition.Column('signup_date', SqlType.date(), NOT_NULLABLE),
    TableDefinition.Column('country_name', SqlType.text(), NOT_NULLABLE),
    TableDefinition.Column('product_name', SqlType.text(), NOT_NULLABLE),
    TableDefinition.Column('category_name', SqlType.text(), NOT_NULLABLE),
])

with create_engine(PG_URL).connect() as pg:
    rows_in = pg.execute(text(SQL)).all()       # money stays Decimal, dates stay dates
path = Path('meridian.hyper')
with HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(hyper.endpoint, path, CreateMode.CREATE_AND_REPLACE) as conn:
        conn.catalog.create_schema('Extract')
        conn.catalog.create_table(ORDERS)
        with Inserter(conn, ORDERS) as inserter:
            inserter.add_rows(rows_in)
            inserter.execute()
        rows = conn.execute_scalar_query('SELECT COUNT(*) FROM "Extract"."orders"')
print(f'{path}: {rows:,} rows, {path.stat().st_size:,} bytes')
