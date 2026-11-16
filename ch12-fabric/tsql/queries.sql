-- Run on the lakehouse's SQL analytics endpoint (Step 5). Also tested on SQL Server 2022.

-- 1. Revenue by country, completed orders of 2023
SELECT c.country_name,
       COUNT(*)            AS orders,
       SUM(o.total_amount) AS revenue
FROM dbo.fact_orders AS o
JOIN dbo.dim_customer AS cu ON cu.customer_id = o.customer_id
JOIN dbo.dim_country  AS c  ON c.country_id  = cu.country_id
WHERE o.status = 'completed'
  AND o.order_date >= '2023-01-01' AND o.order_date < '2024-01-01'
GROUP BY c.country_name
ORDER BY revenue DESC;

-- 2. Monthly revenue of 2023 with a running total
SELECT DATETRUNC(month, order_date) AS order_month,
       SUM(total_amount)            AS revenue,
       SUM(SUM(total_amount))
           OVER (ORDER BY DATETRUNC(month, order_date))
                                    AS running_total
FROM dbo.fact_orders
WHERE status = 'completed'
  AND order_date >= '2023-01-01' AND order_date < '2024-01-01'
GROUP BY DATETRUNC(month, order_date)
ORDER BY order_month;
