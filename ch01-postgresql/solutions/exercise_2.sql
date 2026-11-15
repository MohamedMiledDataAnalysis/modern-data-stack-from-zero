-- Chapter 1 — correction to Exercise 2
SELECT ca.category_name, COUNT(*) AS returned_orders
FROM fact_orders fo
JOIN dim_product  dp ON fo.product_id  = dp.product_id
JOIN dim_category ca ON dp.category_id = ca.category_id
WHERE fo.status = 'returned'
GROUP BY ca.category_name
ORDER BY returned_orders DESC
LIMIT 5;
