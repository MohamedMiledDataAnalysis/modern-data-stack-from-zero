-- Exercise 3: completed revenue per category
select
    category_name,
    count(*)           as orders,
    sum(total_amount)  as revenue
from {{ ref('int_orders_enriched') }}
where status = 'completed'
group by category_name
order by revenue desc
