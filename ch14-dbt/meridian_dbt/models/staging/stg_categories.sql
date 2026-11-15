-- One row per category, unchanged from the source
select *
from {{ source('meridian', 'dim_category') }}
