-- Foundation 3: the four database objects on Meridian (table, view, procedure, function).
-- Run after Chapter 1:  psql -h localhost -U meridian_user meridian_db -f foundations/f3_database_objects.sql
-- It removes what it creates at the end, so it can be run any number of times.

-- A view: a saved query
CREATE VIEW completed_orders AS
SELECT * FROM fact_orders WHERE status = 'completed';

SELECT COUNT(*) AS completed FROM completed_orders;   -- 150311

-- A stored procedure: a named block of statements, run with CALL
CREATE TABLE daily_sales (order_date DATE PRIMARY KEY,
                          revenue NUMERIC(12,2));

CREATE PROCEDURE refresh_daily_sales()
LANGUAGE sql
AS $$
  TRUNCATE daily_sales;
  INSERT INTO daily_sales
  SELECT order_date, SUM(total_amount)
  FROM fact_orders
  WHERE status = 'completed'
  GROUP BY order_date;
$$;

CALL refresh_daily_sales();

SELECT COUNT(*) AS days, SUM(revenue) AS revenue FROM daily_sales;
-- 1096 days, 108118520.21

-- A function: takes inputs, returns a value used inside a query
CREATE FUNCTION vat(amount NUMERIC) RETURNS NUMERIC
LANGUAGE sql
AS $$ SELECT ROUND(amount * 0.20, 2) $$;

SELECT order_id, total_amount, vat(total_amount)
FROM fact_orders
ORDER BY order_id
LIMIT 3;

-- Clean up
DROP FUNCTION vat(NUMERIC);
DROP PROCEDURE refresh_daily_sales();
DROP TABLE daily_sales;
DROP VIEW completed_orders;
