-- Spark SQL (Chapters 13 and 15). Run with run_spark.py.

-- 1. Cut dates down to the month
SELECT CAST(DATE_TRUNC('MONTH', order_date) AS DATE) AS month,
       COUNT(*) AS orders, SUM(total_amount) AS revenue
FROM fact_orders
WHERE status = 'completed' AND order_date BETWEEN '2023-01-01' AND '2023-03-31'
GROUP BY 1 ORDER BY 1;

-- 2. Keep the first rows
SELECT order_id, total_amount
FROM fact_orders
WHERE order_date BETWEEN '2023-01-01' AND '2023-03-31'
ORDER BY total_amount DESC, order_id
LIMIT 3;

-- 3. Join text
SELECT customer_id, CONCAT(first_name, ' ', last_name) AS full_name
FROM dim_customer WHERE customer_id <= 2 ORDER BY customer_id;

-- 4. Compare each month with the previous one
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS previous,
       SUM(revenue) OVER (ORDER BY month) AS running_total
FROM (SELECT CAST(DATE_TRUNC('MONTH', order_date) AS DATE) AS month, SUM(total_amount) AS revenue
      FROM fact_orders
      WHERE status = 'completed' AND order_date BETWEEN '2023-01-01' AND '2023-03-31'
      GROUP BY 1) AS m
ORDER BY month;

-- 5. The best-selling product of each category: QUALIFY, ordering by the alias `revenue`
SELECT p.category_id, o.product_id, SUM(o.total_amount) AS revenue
FROM fact_orders o JOIN dim_product p ON p.product_id = o.product_id
WHERE o.status = 'completed' AND o.order_date BETWEEN '2023-01-01' AND '2023-03-31'
  AND p.category_id <= 3
GROUP BY p.category_id, o.product_id
QUALIFY ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY revenue DESC) = 1
ORDER BY p.category_id;
