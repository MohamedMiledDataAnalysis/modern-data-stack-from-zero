"""Chapter 10 corrections, Exercises 1 and 2. Run from the ch10-snowflake folder:
    python solutions/exercises.py
Exercise 3 (Time Travel) runs only on a real Snowflake account: see the book.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sf_config import sf_connect                       # noqa: E402

conn = sf_connect()
cur = conn.cursor()

print('Exercise 1 - share of returned orders per country, 2023')
cur.execute("""
    SELECT c.COUNTRY_NAME,
           COUNT_IF(o.STATUS = 'returned') AS RETURNED,
           COUNT(*) AS ORDERS,
           ROUND(100 * COUNT_IF(o.STATUS = 'returned') / COUNT(*), 1) AS PCT
    FROM FACT_ORDERS o
    JOIN DIM_CUSTOMER cu ON cu.CUSTOMER_ID = o.CUSTOMER_ID
    JOIN DIM_COUNTRY  c  ON c.COUNTRY_ID  = cu.COUNTRY_ID
    WHERE YEAR(o.ORDER_DATE) = 2023
    GROUP BY c.COUNTRY_NAME
    ORDER BY PCT DESC, c.COUNTRY_NAME""")
for country, returned, orders, pct in cur.fetchall():
    print(f'{country:<12}{int(returned):>6}{orders:>7}{float(pct):>6.1f}')

print('Exercise 2 - a clone is independent of its source')
cur.execute('DROP TABLE IF EXISTS FACT_ORDERS_DEV')
cur.execute('CREATE TABLE FACT_ORDERS_DEV CLONE FACT_ORDERS')
cur.execute("UPDATE FACT_ORDERS_DEV SET STATUS = 'test' WHERE ORDER_ID < 100")
cur.execute("""SELECT (SELECT COUNT(*) FROM FACT_ORDERS_DEV WHERE STATUS = 'test'),
                      (SELECT COUNT(*) FROM FACT_ORDERS     WHERE STATUS = 'test')""")
print('test rows in clone, in source:', cur.fetchone())
cur.execute('DROP TABLE FACT_ORDERS_DEV')
conn.close()
