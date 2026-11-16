-- The figures each Data Studio (formerly Looker Studio) chart of Chapter 25 must show, computed in PostgreSQL
-- on the same flat table.
WITH f AS (
    SELECT o.order_id, o.order_date, o.status, o.total_amount, o.customer_id,
           c.country_name, cat.category_name
    FROM fact_orders o
    JOIN dim_customer cu ON cu.customer_id = o.customer_id
    JOIN dim_country  c  ON c.country_id   = cu.country_id
    JOIN dim_product  p  ON p.product_id   = o.product_id
    JOIN dim_category cat ON cat.category_id = p.category_id)
SELECT 'Scorecards, 2023' AS view, NULL AS label,
       SUM(total_amount) FILTER (WHERE status = 'completed') AS value_1,
       COUNT(DISTINCT customer_id) AS value_2
FROM f WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'
UNION ALL
SELECT 'Exercise 1 - cancelled share, 2023', country_name,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'cancelled') / COUNT(*), 2), NULL
FROM f WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY country_name
UNION ALL
SELECT 'Exercise 2 - completed revenue, December 2023', category_name,
       SUM(total_amount) FILTER (WHERE status = 'completed'), NULL
FROM f WHERE order_date BETWEEN '2023-12-01' AND '2023-12-31' GROUP BY category_name
ORDER BY 1, 3 DESC;
