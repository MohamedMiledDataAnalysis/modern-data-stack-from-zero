-- The figures each Power BI visual of Chapter 24 must show, computed in PostgreSQL.
-- psql -h localhost -U meridian_user meridian_db -f check_figures.sql

-- Step 5: [Revenue] and [Return rate] per year
SELECT EXTRACT(YEAR FROM order_date) AS year,
       SUM(total_amount) FILTER (WHERE status = 'completed') AS revenue,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'returned') / COUNT(*), 2) AS return_rate_pct
FROM fact_orders GROUP BY 1 ORDER BY 1;

-- Step 6: [Revenue YoY %] per country, 2023 against 2022
WITH r AS (
    SELECT c.country_name, EXTRACT(YEAR FROM o.order_date) AS year, SUM(o.total_amount) AS revenue
    FROM fact_orders o
    JOIN dim_customer cu USING (customer_id)
    JOIN dim_country c ON c.country_id = cu.country_id
    WHERE o.status = 'completed' AND EXTRACT(YEAR FROM o.order_date) IN (2022, 2023)
    GROUP BY 1, 2)
SELECT a.country_name, a.revenue AS revenue_2023, b.revenue AS revenue_2022,
       ROUND(100 * (a.revenue - b.revenue) / b.revenue, 2) AS yoy_pct
FROM r a JOIN r b ON a.country_name = b.country_name AND a.year = 2023 AND b.year = 2022
UNION ALL
SELECT 'Total', SUM(total_amount) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2023),
       SUM(total_amount) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2022),
       ROUND(100 * (SUM(total_amount) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2023)
                  - SUM(total_amount) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2022))
                  / SUM(total_amount) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2022), 2)
FROM fact_orders WHERE status = 'completed'
ORDER BY yoy_pct DESC;

-- Exercise 1: [Orders] and [Average order] per category, completed orders of 2023 (top 3)
SELECT cat.category_name, COUNT(*) AS orders, ROUND(AVG(o.total_amount), 2) AS avg_order
FROM fact_orders o JOIN dim_product p USING (product_id) JOIN dim_category cat USING (category_id)
WHERE o.status = 'completed' AND o.order_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY 1 ORDER BY avg_order DESC LIMIT 3;

-- Exercise 2: cumulative revenue of 2023 at the end of each quarter (TOTALYTD)
SELECT DISTINCT EXTRACT(QUARTER FROM order_date) AS quarter,
       SUM(total_amount) OVER (ORDER BY EXTRACT(QUARTER FROM order_date)) AS ytd
FROM fact_orders
WHERE status = 'completed' AND order_date BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY quarter;

-- Exercise 3: rank of each product category by 2023 revenue (RANKX), first four
SELECT cat.category_name, SUM(o.total_amount) AS revenue,
       RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS rank
FROM fact_orders o JOIN dim_product p USING (product_id) JOIN dim_category cat USING (category_id)
WHERE o.status = 'completed' AND o.order_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY 1 ORDER BY rank LIMIT 4;
