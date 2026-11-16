-- Chapter 1 — the queries of Steps 4 to 7, in order
SELECT order_id, quantity, unit_price, total_amount, status
FROM fact_orders
ORDER BY order_id
LIMIT 5;

SELECT order_id, total_amount
FROM fact_orders
WHERE status = 'returned'
ORDER BY total_amount DESC, order_id
LIMIT 3;

SELECT status, COUNT(*) AS order_count
FROM fact_orders
GROUP BY status
ORDER BY order_count DESC;

SELECT c.first_name, c.last_name, co.country_name
FROM dim_customer c
JOIN dim_country co ON c.country_id = co.country_id
WHERE c.customer_id <= 3
ORDER BY c.customer_id;

SELECT co.country_name,
       ROUND(AVG(fo.total_amount), 2) AS avg_order_value
FROM fact_orders fo
JOIN dim_customer cu ON fo.customer_id = cu.customer_id
JOIN dim_country co  ON cu.country_id  = co.country_id
WHERE fo.status = 'completed'
GROUP BY co.country_name
ORDER BY avg_order_value DESC;
