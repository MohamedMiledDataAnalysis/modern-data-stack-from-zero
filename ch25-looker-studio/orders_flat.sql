-- One flat table for Looker Studio: each order with its country and category.
-- In BigQuery (Step 2) replace the table names by `meridian-2026.meridian.<table>`.
SELECT o.order_id, o.order_date, o.status, o.quantity, o.total_amount,
       o.customer_id, c.country_name, cat.category_name
FROM fact_orders o
JOIN dim_customer cu ON cu.customer_id = o.customer_id
JOIN dim_country  c  ON c.country_id   = cu.country_id
JOIN dim_product  p  ON p.product_id   = o.product_id
JOIN dim_category cat ON cat.category_id = p.category_id
