-- Builds, in your own PostgreSQL, the tables Fivetran would create,
-- so that the queries of Chapter 6 can be practised without an account.
DROP SCHEMA IF EXISTS meridian_public CASCADE;
CREATE SCHEMA meridian_public;

CREATE TABLE meridian_public.fact_orders AS
SELECT o.*,
       TIMESTAMPTZ '2026-11-15 02:00:00+00' AS _fivetran_synced,
       FALSE AS _fivetran_deleted
FROM public.fact_orders o;

-- The next sync, a day later: 3 orders change status, 1 is deleted in the source.
UPDATE meridian_public.fact_orders
SET status = 'returned', _fivetran_synced = TIMESTAMPTZ '2026-11-16 02:00:00+00'
WHERE order_id IN (10, 20, 30);
UPDATE meridian_public.fact_orders
SET _fivetran_deleted = TRUE, _fivetran_synced = TIMESTAMPTZ '2026-11-16 02:00:00+00'
WHERE order_id = 40;

-- dim_customer in history mode: customer 7 moved country on 16 November.
CREATE TABLE meridian_public.dim_customer AS
SELECT c.*,
       TIMESTAMPTZ '2026-11-15 02:00:00+00' AS _fivetran_start,
       TIMESTAMPTZ '9999-12-31 23:59:59.999+00' AS _fivetran_end,
       TRUE AS _fivetran_active,
       TIMESTAMPTZ '2026-11-15 02:00:00+00' AS _fivetran_synced
FROM public.dim_customer c;
UPDATE meridian_public.dim_customer
SET _fivetran_end = TIMESTAMPTZ '2026-11-16 08:59:59.999+00', _fivetran_active = FALSE
WHERE customer_id = 7;
INSERT INTO meridian_public.dim_customer
SELECT customer_id, first_name, last_name, email, 3, signup_date,
       TIMESTAMPTZ '2026-11-16 09:00:00+00', TIMESTAMPTZ '9999-12-31 23:59:59.999+00',
       TRUE, TIMESTAMPTZ '2026-11-16 10:00:00+00'
FROM public.dim_customer WHERE customer_id = 7;
