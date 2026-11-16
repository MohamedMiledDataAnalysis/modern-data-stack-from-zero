"""Load the Meridian Retail tables into PostgreSQL from the CSV files in data/meridian/.

The Modern Data Stack, Second Edition, Chapter 1.
An alternative to generate_meridian.py: both create the same five tables with
the same rows. Use this one if you prefer to start from the files.

Running it again rebuilds the five tables from scratch, like the generator: the
DROP ... CASCADE also removes anything later chapters built on them.

Run from the repository folder:  python data/load_meridian_csv.py
"""
from pathlib import Path

import psycopg2

from generate_meridian import DDL   # the same table definitions as the generator

TABLES = ['dim_country', 'dim_category', 'dim_customer', 'dim_product', 'fact_orders']
SRC = Path(__file__).parent / 'meridian'


def main():
    conn = psycopg2.connect(dbname='meridian_db', user='meridian_user',
                            password='meridian2024', host='localhost')
    cur = conn.cursor()
    cur.execute(DDL)
    for table in TABLES:            # dimensions first: fact_orders refers to them
        with open(SRC / f'{table}.csv', encoding='utf-8') as f:
            cur.copy_expert(f'COPY {table} FROM STDIN WITH (FORMAT csv, HEADER)', f)
        cur.execute(f'SELECT COUNT(*) FROM {table}')
        print(f'{table:<13} {cur.fetchone()[0]:>7,} rows loaded')
    # the two SERIAL columns continue after the loaded ids
    cur.execute("SELECT setval('dim_country_country_id_seq', (SELECT MAX(country_id) FROM dim_country))")
    cur.execute("SELECT setval('dim_category_category_id_seq', (SELECT MAX(category_id) FROM dim_category))")
    conn.commit()
    print('Done. Meridian Retail database is ready.')
    conn.close()


if __name__ == '__main__':
    main()
