"""Chapter 11 corrections. Run from the ch11-bigquery folder:
    python solutions/exercises.py        all three
    python solutions/exercises.py 2      Exercise 2 only
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from google.cloud import bigquery                      # noqa: E402

from bq_config import DATASET, PROJECT, bq_client      # noqa: E402

client = bq_client()
T = f'`{PROJECT}.{DATASET}`'


def exercise_1():
    print('Exercise 1 - monthly completed revenue, first quarter of 2023')
    sql = f"""
    SELECT DATE_TRUNC(order_date, MONTH) AS month,
           COUNT(*) AS orders,
           ROUND(SUM(total_amount), 2) AS revenue
    FROM {T}.fact_orders
    WHERE status = 'completed' AND order_date BETWEEN '2023-01-01' AND '2023-03-31'
    GROUP BY month ORDER BY month"""
    for r in client.query(sql).result():
        print(r.month, r.orders, f'{float(r.revenue):,.2f}')


def exercise_2():
    print('Exercise 2 - query parameters instead of string formatting')
    sql = f"""
    SELECT COUNT(*) AS n FROM {T}.fact_orders
    WHERE status = @status AND order_date BETWEEN @first_day AND @last_day"""
    config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter('status', 'STRING', 'returned'),
        bigquery.ScalarQueryParameter('first_day', 'DATE', '2023-03-01'),
        bigquery.ScalarQueryParameter('last_day', 'DATE', '2023-03-31'),
    ])
    print(list(client.query(sql, job_config=config).result())[0].n)


def exercise_3():
    print('Exercise 3 - top 3 products by revenue in each category, first quarter of 2023')
    sql = f"""
    SELECT cat.category_name, p.product_name,
           ROUND(SUM(o.total_amount), 2) AS revenue
    FROM {T}.fact_orders AS o
    JOIN {T}.dim_product AS p USING (product_id)
    JOIN {T}.dim_category AS cat USING (category_id)
    WHERE o.status = 'completed' AND o.order_date BETWEEN '2023-01-01' AND '2023-03-31'
    GROUP BY cat.category_name, p.product_name
    QUALIFY ROW_NUMBER() OVER (PARTITION BY cat.category_name
                               ORDER BY SUM(o.total_amount) DESC) <= 3
    ORDER BY cat.category_name, revenue DESC
    LIMIT 6"""
    for r in client.query(sql).result():
        print(f'{r.category_name:<14}{r.product_name:<14}{float(r.revenue):>12,.2f}')


chosen = sys.argv[1] if len(sys.argv) > 1 else '123'
for n in chosen:
    {'1': exercise_1, '2': exercise_2, '3': exercise_3}[n]()
