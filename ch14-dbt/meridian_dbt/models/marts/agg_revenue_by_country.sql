-- agg_revenue_by_country.sql
-- Completed revenue per country and year
select
    country_name,
    extract(year from order_date)::integer  as order_year,
    count(*)                                as orders,
    sum(total_amount)                       as revenue
from {{ ref('int_orders_enriched') }}
where status = 'completed'
group by country_name, extract(year from order_date)
order by country_name, order_year
