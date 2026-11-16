"""Generate the Meridian Retail dataset and load it into PostgreSQL.

The Modern Data Stack, Second Edition, Chapter 1.
Seed 42 with Faker 40.54.0 gives every reader identical data.

Running it again rebuilds the five tables from scratch. The DROP ... CASCADE also removes
anything later chapters built on them, such as dbt views (Chapter 14): rerun those chapters'
steps afterwards.
"""
import random
from datetime import date, timedelta

import psycopg2
from psycopg2.extras import execute_values
from faker import Faker

SEED = 42
random.seed(SEED)
fake = Faker(['en_GB', 'fr_FR', 'de_DE', 'es_ES', 'it_IT', 'nl_NL'])
Faker.seed(SEED)

COUNTRIES = ['UK', 'France', 'Germany', 'Spain', 'Italy', 'Netherlands']
CATEGORIES = ['Electronics', 'Home & Garden', 'Clothing', 'Sports', 'Books',
              'Toys', 'Beauty', 'Automotive', 'Food', 'Music', 'Office', 'Pets']
STATUSES = ['completed', 'completed', 'completed', 'returned', 'cancelled']
START = date(2021, 1, 1)

DDL = '''
DROP TABLE IF EXISTS fact_orders, dim_product, dim_customer,
                     dim_category, dim_country CASCADE;
CREATE TABLE dim_country (
  country_id   SERIAL PRIMARY KEY,
  country_name VARCHAR(50) NOT NULL UNIQUE);
CREATE TABLE dim_category (
  category_id   SERIAL PRIMARY KEY,
  category_name VARCHAR(50) NOT NULL UNIQUE);
CREATE TABLE dim_customer (
  customer_id INTEGER PRIMARY KEY,
  first_name  VARCHAR(50)  NOT NULL,
  last_name   VARCHAR(50)  NOT NULL,
  email       VARCHAR(100) NOT NULL UNIQUE,
  country_id  INTEGER REFERENCES dim_country(country_id),
  signup_date DATE NOT NULL);
CREATE TABLE dim_product (
  product_id   INTEGER PRIMARY KEY,
  product_name VARCHAR(100) NOT NULL,
  category_id  INTEGER REFERENCES dim_category(category_id),
  unit_price   NUMERIC(8,2) NOT NULL);
CREATE TABLE fact_orders (
  order_id     INTEGER PRIMARY KEY,
  customer_id  INTEGER REFERENCES dim_customer(customer_id),
  product_id   INTEGER REFERENCES dim_product(product_id),
  order_date   DATE NOT NULL,
  quantity     INTEGER NOT NULL,
  unit_price   NUMERIC(8,2) NOT NULL,
  total_amount NUMERIC(10,2) NOT NULL,
  status       VARCHAR(20) NOT NULL);
'''


def main():
    conn = psycopg2.connect(dbname='meridian_db', user='meridian_user',
                            password='meridian2024', host='localhost')
    cur = conn.cursor()
    cur.execute(DDL)

    execute_values(cur, 'INSERT INTO dim_country(country_name) VALUES %s',
                   [(c,) for c in COUNTRIES])
    execute_values(cur, 'INSERT INTO dim_category(category_name) VALUES %s',
                   [(c,) for c in CATEGORIES])
    country_id = {c: i for i, c in enumerate(COUNTRIES, 1)}
    category_id = {c: i for i, c in enumerate(CATEGORIES, 1)}

    customers = []
    for i in range(1, 10001):
        country = random.choice(COUNTRIES)
        signup = START + timedelta(days=random.randint(0, 730))
        customers.append((i, fake.first_name(), fake.last_name(),
                          f'user{i}@meridian.example',
                          country_id[country], signup))
    execute_values(cur, 'INSERT INTO dim_customer VALUES %s', customers)
    print('Customers loaded.')

    products, price_of = [], {}
    for i in range(1, 501):
        cat = random.choice(CATEGORIES)
        price = round(random.uniform(2.99, 499.99), 2)
        price_of[i] = price
        products.append((i, f'Product {i:04d}', category_id[cat], price))
    execute_values(cur, 'INSERT INTO dim_product VALUES %s', products)
    print('Products loaded.')

    orders = []
    for i in range(1, 250001):
        prod = random.randint(1, 500)
        price = price_of[prod]
        qty = random.randint(1, 5)
        odate = START + timedelta(days=random.randint(0, 1095))
        orders.append((i, random.randint(1, 10000), prod, odate, qty,
                       price, round(price * qty, 2), random.choice(STATUSES)))
        if i % 50000 == 0:
            execute_values(cur, 'INSERT INTO fact_orders VALUES %s', orders)
            orders = []
            print(f'{i:,} orders loaded...')
    conn.commit()
    print('Done. Meridian Retail database is ready.')
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
