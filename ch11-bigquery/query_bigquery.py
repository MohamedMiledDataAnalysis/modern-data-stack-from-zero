"""Revenue by country in 2023, and the bytes the query read."""
from bq_config import DATASET, PROJECT, bq_client

client = bq_client()
SQL = f"""
SELECT c.country_name,
       ROUND(SUM(o.total_amount), 2) AS revenue
FROM `{PROJECT}.{DATASET}.fact_orders` AS o
JOIN `{PROJECT}.{DATASET}.dim_customer` AS cu USING (customer_id)
JOIN `{PROJECT}.{DATASET}.dim_country` AS c ON c.country_id = cu.country_id
WHERE o.status = 'completed'
  AND o.order_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY c.country_name
ORDER BY revenue DESC
"""
job = client.query(SQL)
for row in job.result():
    print(f'{row.country_name:<12}{float(row.revenue):>14,.2f}')
print('bytes billed:', job.total_bytes_billed)

df = client.query(f'SELECT status, COUNT(*) AS n FROM `{PROJECT}.{DATASET}.fact_orders` '
                  'GROUP BY status ORDER BY n DESC').to_dataframe()
print(df)
