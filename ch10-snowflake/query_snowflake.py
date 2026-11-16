"""Revenue by year and country, computed inside Snowflake."""
from sf_config import sf_connect

SQL = """
SELECT YEAR(o.ORDER_DATE) AS YEAR, c.COUNTRY_NAME,
       ROUND(SUM(o.TOTAL_AMOUNT), 2) AS REVENUE
FROM FACT_ORDERS o
JOIN DIM_CUSTOMER cu ON cu.CUSTOMER_ID = o.CUSTOMER_ID
JOIN DIM_COUNTRY  c  ON c.COUNTRY_ID  = cu.COUNTRY_ID
WHERE o.STATUS = 'completed' AND YEAR(o.ORDER_DATE) = 2023
GROUP BY 1, 2
ORDER BY REVENUE DESC
"""
conn = sf_connect()
cur = conn.cursor()
cur.execute(SQL)
for year, country, revenue in cur.fetchall():
    print(f'{year}  {country:<12}{float(revenue):>14,.2f}')

df = conn.cursor().execute('SELECT STATUS, COUNT(*) AS N FROM FACT_ORDERS '
                           'GROUP BY STATUS ORDER BY N DESC').fetch_pandas_all()
print(df)
conn.close()
