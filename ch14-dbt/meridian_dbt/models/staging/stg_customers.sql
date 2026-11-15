-- One row per customer, unchanged from the source
select *
from {{ source('meridian', 'dim_customer') }}
