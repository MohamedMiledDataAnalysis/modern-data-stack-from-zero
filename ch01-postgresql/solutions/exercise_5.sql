-- Chapter 1 — correction to Exercise 5
SELECT COUNT(*)
FROM dim_customer c
LEFT JOIN fact_orders fo ON c.customer_id = fo.customer_id
WHERE fo.order_id IS NULL;
