-- Chapter 12 corrections. Tested on SQL Server 2022; the same T-SQL runs on the Fabric SQL endpoint.

-- Exercise 1 - the five customers with the highest completed revenue in 2023
SELECT TOP 5 cu.customer_id, cu.first_name, cu.last_name,
       COUNT(*) AS orders, SUM(o.total_amount) AS revenue
FROM dbo.fact_orders AS o
JOIN dbo.dim_customer AS cu ON cu.customer_id = o.customer_id
WHERE o.status = 'completed'
  AND o.order_date >= '2023-01-01' AND o.order_date < '2024-01-01'
GROUP BY cu.customer_id, cu.first_name, cu.last_name
ORDER BY revenue DESC;

-- Exercise 2 - growth of completed revenue per country, 2022 to 2023
WITH yearly AS (
    SELECT c.country_name, YEAR(o.order_date) AS order_year, SUM(o.total_amount) AS revenue
    FROM dbo.fact_orders AS o
    JOIN dbo.dim_customer AS cu ON cu.customer_id = o.customer_id
    JOIN dbo.dim_country  AS c  ON c.country_id  = cu.country_id
    WHERE o.status = 'completed' AND YEAR(o.order_date) IN (2022, 2023)
    GROUP BY c.country_name, YEAR(o.order_date)
)
SELECT country_name, order_year, revenue,
       LAG(revenue) OVER (PARTITION BY country_name ORDER BY order_year) AS previous,
       CAST(100.0 * (revenue - LAG(revenue) OVER (PARTITION BY country_name ORDER BY order_year))
            / LAG(revenue) OVER (PARTITION BY country_name ORDER BY order_year) AS DECIMAL(5,1)) AS growth_pct
FROM yearly
ORDER BY country_name, order_year;
