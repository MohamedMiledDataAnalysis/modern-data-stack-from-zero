"""Chapter 11 corrections. Run from the ch11-bigquery folder: python solutions/exercises.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from google.cloud import bigquery                      # noqa: E402

from bq_config import DATASET, PROJECT, bq_client      # noqa: E402

client = bq_client()
T = f'`{PROJECT}.{DATASET}`'

print('Exercise 1 - monthly completed revenue, first quarter of 2023')
sql = f"""
SELECT FORMAT_DATE('%Y-%m', order_date) AS month,
       COUNT(*) AS orders,
       ROUND(SUM(total_amount), 2) AS revenue
FROM {T}.fact_orders
WHERE status = 'completed' AND order_date BETWEEN '2023-01-01' AND '2023-03-31'
GROUP BY month ORDER BY month"""
for r in client.query(sql).result():
    print(r.month, r.orders, f'{float(r.revenue):,.2f}')

print('Exercise 2 - a query parameter instead of string formatting')
sql = f"""
SELECT COUNT(*) AS n FROM {T}.fact_orders
WHERE status = @status AND order_date >= @since"""
config = bigquery.QueryJobConfig(query_parameters=[
    bigquery.ScalarQueryParameter('status', 'STRING', 'returned'),
    bigquery.ScalarQueryParameter('since', 'DATE', '2023-07-01'),
])
print(list(client.query(sql, job_config=config).result())[0].n)

print('Exercise 3 - top 3 products by revenue in each category, 2023')
sql = f"""
SELECT category_name, product_name, revenue
FROM (
  SELECT cat.category_name, p.product_name,
         ROUND(SUM(o.total_amount), 2) AS revenue,
         ROW_NUMBER() OVER (PARTITION BY cat.category_name
                            ORDER BY SUM(o.total_amount) DESC) AS rank_in_category
  FROM {T}.fact_orders AS o
  JOIN {T}.dim_product AS p USING (product_id)
  JOIN {T}.dim_category AS cat USING (category_id)
  WHERE o.status = 'completed' AND EXTRACT(YEAR FROM o.order_date) = 2023
  GROUP BY cat.category_name, p.product_name
)
WHERE rank_in_category <= 3
ORDER BY category_name, revenue DESC
LIMIT 6"""
for r in client.query(sql).result():
    print(f'{r.category_name:<14}{r.product_name:<14}{float(r.revenue):>12,.2f}')
