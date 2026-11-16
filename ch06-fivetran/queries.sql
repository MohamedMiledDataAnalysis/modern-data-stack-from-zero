-- 1. Rows changed by the latest sync, ignoring deleted rows
SELECT order_id, status, _fivetran_synced
FROM meridian_public.fact_orders
WHERE _fivetran_synced >= TIMESTAMPTZ '2026-11-16 00:00:00+00'
  AND NOT _fivetran_deleted
ORDER BY order_id;

-- 2. Rows deleted in the source (soft delete)
SELECT order_id FROM meridian_public.fact_orders WHERE _fivetran_deleted;

-- 3. History mode: every version of customer 7
SELECT customer_id, country_id, _fivetran_start, _fivetran_end, _fivetran_active
FROM meridian_public.dim_customer
WHERE customer_id = 7
ORDER BY _fivetran_start;

-- 4. History mode: the customer table as it was at a point in time
SELECT country_id, COUNT(*) AS customers
FROM meridian_public.dim_customer
WHERE TIMESTAMPTZ '2026-11-15 12:00:00+00' BETWEEN _fivetran_start AND _fivetran_end
GROUP BY country_id ORDER BY country_id;
