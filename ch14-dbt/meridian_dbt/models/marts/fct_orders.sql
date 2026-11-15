-- fct_orders.sql
-- The order table that Tableau, Power BI
-- and the churn model read
select *
from {{ ref('int_orders_enriched') }}
