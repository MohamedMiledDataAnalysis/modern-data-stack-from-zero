"""The figures each Tableau view of Chapter 23 must show, computed with SQL on meridian.hyper.
Run from the ch23-tableau folder after build_extract.py."""
from tableauhyperapi import Connection, HyperProcess, Telemetry

QUERIES = {
    'Step 4 - completed revenue per country, 2023': """
        SELECT country_name, SUM(total_amount) AS revenue
        FROM "Extract"."orders"
        WHERE status = 'completed' AND EXTRACT(YEAR FROM order_date) = 2023
        GROUP BY country_name ORDER BY revenue DESC""",
    'Step 5 - return rate per category (top 3)': """
        SELECT category_name,
               CAST(100.0 * SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) / COUNT(*) AS NUMERIC(5,2)) AS pct
        FROM "Extract"."orders"
        GROUP BY category_name ORDER BY pct DESC LIMIT 3""",
    'Step 6 - average customer lifetime revenue per country (INCLUDE LOD)': """
        SELECT country_name, ROUND(AVG(lifetime), 2) AS avg_lifetime FROM (
            SELECT customer_id, MIN(country_name) AS country_name,
                   SUM(CASE WHEN status = 'completed' THEN total_amount ELSE 0 END) AS lifetime
            FROM "Extract"."orders" GROUP BY customer_id) AS c
        GROUP BY country_name ORDER BY avg_lifetime DESC""",
    'Exercise 1 - average completed order value per country, 2023': """
        SELECT country_name, ROUND(AVG(total_amount), 2) AS avg_order
        FROM "Extract"."orders"
        WHERE status = 'completed' AND EXTRACT(YEAR FROM order_date) = 2023
        GROUP BY country_name ORDER BY avg_order DESC""",
    'Exercise 2 - share of each country in 2023 completed revenue (%)': """
        SELECT country_name,
               CAST(100.0 * SUM(total_amount) / SUM(SUM(total_amount)) OVER () AS NUMERIC(5,2)) AS pct
        FROM "Extract"."orders"
        WHERE status = 'completed' AND EXTRACT(YEAR FROM order_date) = 2023
        GROUP BY country_name ORDER BY pct DESC""",
    'Exercise 3 - customers whose first order is earlier than their sign-up date': """
        SELECT COUNT(*) FROM (
            SELECT customer_id, MIN(order_date) AS first_order, MIN(signup_date) AS signup
            FROM "Extract"."orders" GROUP BY customer_id) AS w
        WHERE first_order < signup""",
}

with HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(hyper.endpoint, 'meridian.hyper') as conn:
        for title, sql in QUERIES.items():
            print(title)
            for row in conn.execute_list_query(sql):
                print('   ', *row)
