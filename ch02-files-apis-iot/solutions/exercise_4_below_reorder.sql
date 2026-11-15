-- Exercise 4 — products below their reorder level, by category
SELECT c.category_name, COUNT(*) AS products_to_reorder
FROM supplier_stock s
JOIN dim_product  p ON s.product_id  = p.product_id
JOIN dim_category c ON p.category_id = c.category_id
WHERE s.stock_qty < s.reorder_level
GROUP BY c.category_name
ORDER BY products_to_reorder DESC, c.category_name
LIMIT 3;
