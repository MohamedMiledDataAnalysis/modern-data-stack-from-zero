-- One row per country, unchanged from the source
select *
from {{ source('meridian', 'dim_country') }}
