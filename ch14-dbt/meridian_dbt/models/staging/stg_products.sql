-- One row per product, unchanged from the source
select *
from {{ source('meridian', 'dim_product') }}
