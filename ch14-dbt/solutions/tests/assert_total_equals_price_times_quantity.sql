-- Exercise 4: every order total must equal unit price x quantity.
-- A singular test passes when this query returns no rows.
select order_id, unit_price, quantity, total_amount
from {{ ref('stg_orders') }}
where total_amount <> unit_price * quantity
