-- One row per order, with clean types and lower-case status
select
    order_id::integer            as order_id,
    customer_id::integer         as customer_id,
    product_id::integer          as product_id,
    order_date::date             as order_date,
    quantity::integer            as quantity,
    unit_price::numeric(8,2)     as unit_price,
    total_amount::numeric(10,2)  as total_amount,
    lower(trim(status))          as status
from {{ source('meridian', 'fact_orders') }}
