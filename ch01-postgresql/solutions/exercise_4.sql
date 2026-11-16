-- Chapter 1 — correction to Exercise 4
SELECT COUNT(*)
FROM fact_orders fo
JOIN dim_customer c ON fo.customer_id = c.customer_id
WHERE fo.order_date < c.signup_date;

-- The first three, with both dates
SELECT fo.order_id, fo.order_date, c.signup_date
FROM fact_orders fo
JOIN dim_customer c ON fo.customer_id = c.customer_id
WHERE fo.order_date < c.signup_date
ORDER BY fo.order_id
LIMIT 3;
