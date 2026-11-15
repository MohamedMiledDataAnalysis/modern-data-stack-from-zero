-- Exercise 3 — no customer appears in more than one partition
SELECT customer_id, COUNT(DISTINCT kafka_partition) AS partitions
FROM orders_stream
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY partitions DESC, customer_id
LIMIT 3;
