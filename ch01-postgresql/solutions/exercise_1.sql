-- Chapter 1 — correction to Exercise 1
SELECT TO_CHAR(order_date, 'YYYY-MM') AS month,
       SUM(total_amount)              AS monthly_revenue
FROM fact_orders
WHERE status = 'completed'
GROUP BY month
ORDER BY month;
