-- T-SQL (Chapter 12): the Fabric SQL analytics endpoint, or SQL Server 2022.

-- 1. Cut dates down to the month
SELECT DATETRUNC(month, order_date) AS month,
       COUNT(*) AS orders, SUM(total_amount) AS revenue
FROM dbo.fact_orders
WHERE status = 'completed' AND order_date BETWEEN '2023-01-01' AND '2023-03-31'
GROUP BY DATETRUNC(month, order_date) ORDER BY month;

-- 2. Keep the first rows
SELECT TOP 3 order_id, total_amount
FROM dbo.fact_orders
WHERE order_date BETWEEN '2023-01-01' AND '2023-03-31'
ORDER BY total_amount DESC, order_id;

-- 3. Join text
SELECT customer_id, CONCAT(first_name, ' ', last_name) AS full_name
FROM dbo.dim_customer WHERE customer_id <= 2 ORDER BY customer_id;

-- 4. Compare each month with the previous one
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS previous,
       SUM(revenue) OVER (ORDER BY month) AS running_total
FROM (SELECT DATETRUNC(month, order_date) AS month, SUM(total_amount) AS revenue
      FROM dbo.fact_orders
      WHERE status = 'completed' AND order_date BETWEEN '2023-01-01' AND '2023-03-31'
      GROUP BY DATETRUNC(month, order_date)) AS m
ORDER BY month;

-- 5. The best-selling product of each category: no QUALIFY, so a subquery
SELECT category_id, product_id, revenue FROM (
    SELECT p.category_id, o.product_id, SUM(o.total_amount) AS revenue,
           ROW_NUMBER() OVER (PARTITION BY p.category_id
                              ORDER BY SUM(o.total_amount) DESC) AS rn
    FROM dbo.fact_orders o JOIN dbo.dim_product p ON p.product_id = o.product_id
    WHERE o.status = 'completed' AND o.order_date BETWEEN '2023-01-01' AND '2023-03-31'
    GROUP BY p.category_id, o.product_id) AS ranked
WHERE rn = 1 AND category_id <= 3
ORDER BY category_id;
