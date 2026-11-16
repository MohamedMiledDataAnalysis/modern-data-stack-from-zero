"""Chapter 34 — expose Meridian's health as Prometheus metrics on port 8001."""
import time

import psycopg2
from prometheus_client import Gauge, start_http_server

TABLES = ['fact_orders', 'dim_customer', 'dim_product']

rows = Gauge('meridian_table_rows', 'Number of rows in a Meridian table', ['table'])
orders = Gauge('meridian_orders', 'Orders by status', ['status'])
latest = Gauge('meridian_latest_order_timestamp_seconds',
               'Date of the most recent order, as a Unix timestamp')
bad = Gauge('meridian_quality_failed_rows',
            'Rows breaking a data-quality rule', ['rule'])
scrape_ok = Gauge('meridian_exporter_last_success_timestamp_seconds',
                  'When the exporter last read the database successfully')


def collect():
    with psycopg2.connect(host='localhost', dbname='meridian_db',
                          user='meridian_user', password='meridian2024') as conn:
        with conn.cursor() as cur:
            for t in TABLES:
                cur.execute(f'SELECT COUNT(*) FROM {t}')
                rows.labels(table=t).set(cur.fetchone()[0])
            cur.execute('SELECT status, COUNT(*) FROM fact_orders '
                        'GROUP BY status ORDER BY status')
            for status, n in cur.fetchall():
                orders.labels(status=status).set(n)
            cur.execute('SELECT EXTRACT(EPOCH FROM MAX(order_date)::timestamp) FROM fact_orders')
            latest.set(float(cur.fetchone()[0]))
            cur.execute('SELECT COUNT(*) FROM fact_orders o JOIN dim_customer c '
                        'USING (customer_id) WHERE o.order_date < c.signup_date')
            bad.labels(rule='order_before_signup').set(cur.fetchone()[0])
    scrape_ok.set_to_current_time()


if __name__ == '__main__':
    start_http_server(8001)
    print('Serving metrics on http://localhost:8001/metrics')
    while True:
        try:
            collect()
        except psycopg2.Error as err:
            print('Database error:', err)
        time.sleep(30)
