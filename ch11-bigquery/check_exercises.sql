-- The expected answers of Chapter 11's exercises, computed in PostgreSQL on the same data.
-- psql -h localhost -U meridian_user meridian_db -f check_exercises.sql
SELECT to_char(order_date, 'YYYY-MM') AS month, COUNT(*) AS orders, SUM(total_amount) AS revenue
FROM fact_orders
WHERE status = 'completed' AND order_date BETWEEN '2023-01-01' AND '2023-03-31'
GROUP BY 1 ORDER BY 1;

SELECT COUNT(*) FROM fact_orders
WHERE status = 'returned' AND order_date BETWEEN '2023-03-01' AND '2023-03-31';

SELECT category_name, product_name, revenue FROM (
    SELECT cat.category_name, p.product_name, SUM(o.total_amount) AS revenue,
           ROW_NUMBER() OVER (PARTITION BY cat.category_name ORDER BY SUM(o.total_amount) DESC) AS rn
    FROM fact_orders o JOIN dim_product p USING (product_id) JOIN dim_category cat USING (category_id)
    WHERE o.status = 'completed' AND o.order_date BETWEEN '2023-01-01' AND '2023-03-31'
    GROUP BY 1, 2) AS ranked
WHERE rn <= 3 ORDER BY category_name, revenue DESC LIMIT 6;
