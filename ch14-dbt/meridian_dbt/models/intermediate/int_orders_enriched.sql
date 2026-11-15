-- One row per order, with customer, product,
-- country and category names
select
    o.order_id,
    o.order_date,
    o.quantity,
    o.unit_price,
    o.total_amount,
    o.status,
    o.customer_id,
    c.first_name || ' ' || c.last_name  as customer_name,
    co.country_name,
    o.product_id,
    p.product_name,
    ca.category_name
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c
    on o.customer_id = c.customer_id
join {{ ref('stg_products') }} p
    on o.product_id = p.product_id
join {{ ref('stg_countries') }} co
    on c.country_id = co.country_id
join {{ ref('stg_categories') }} ca
    on p.category_id = ca.category_id
