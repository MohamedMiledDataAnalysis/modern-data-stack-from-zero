import time
from bq_config import DATASET, PROJECT, bq_client
c = bq_client(); T = f'`{PROJECT}.{DATASET}`'
print("start", flush=True)
for sql in [f"SELECT COUNT(*) n FROM {T}.dim_country",
            f"SELECT COUNT(*) n FROM {T}.dim_customer",
            f"SELECT COUNT(*) n FROM {T}.fact_orders",
            f"SELECT status, COUNT(*) n FROM {T}.fact_orders GROUP BY status",
            f"SELECT COUNT(*) n FROM {T}.fact_orders WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'",
            f"SELECT c.country_name, COUNT(*) n FROM {T}.dim_customer cu JOIN {T}.dim_country c ON c.country_id = cu.country_id GROUP BY 1",
            f"SELECT COUNT(*) n FROM {T}.fact_orders o JOIN {T}.dim_customer cu USING (customer_id) WHERE o.order_date BETWEEN '2023-01-01' AND '2023-01-31'"]:
    t = time.time()
    try:
        rows = list(c.query(sql, timeout=120).result(timeout=120))
        print(round(time.time()-t, 1), 's', [tuple(r) for r in rows][:3])
    except Exception as e:
        print(round(time.time()-t, 1), 's ERR', str(e)[:200])
