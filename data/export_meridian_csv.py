"""Save the five Meridian Retail tables from PostgreSQL as CSV files in data/meridian/.

The Modern Data Stack, Second Edition, Chapter 1.
The CSV files in the repository were written by this script, straight after
generate_meridian.py. Rows are sorted by their key, so the files are identical
on every machine.

Run from the repository folder:  python data/export_meridian_csv.py
"""
from pathlib import Path

import psycopg2

TABLES = {                      # table: the column that orders its rows
    'dim_country': 'country_id',
    'dim_category': 'category_id',
    'dim_customer': 'customer_id',
    'dim_product': 'product_id',
    'fact_orders': 'order_id',
}
OUT = Path(__file__).parent / 'meridian'


def main():
    OUT.mkdir(exist_ok=True)
    conn = psycopg2.connect(dbname='meridian_db', user='meridian_user',
                            password='meridian2024', host='localhost')
    cur = conn.cursor()
    for table, key in TABLES.items():
        path = OUT / f'{table}.csv'
        with open(path, 'w', encoding='utf-8', newline='') as f:
            cur.copy_expert(f'COPY (SELECT * FROM {table} ORDER BY {key}) '
                            'TO STDOUT WITH (FORMAT csv, HEADER)', f)
        cur.execute(f'SELECT COUNT(*) FROM {table}')
        print(f'{table:<13} {cur.fetchone()[0]:>7,} rows -> {path.name}')
    conn.close()


if __name__ == '__main__':
    main()
