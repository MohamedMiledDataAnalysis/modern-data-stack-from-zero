select * from {{ source('meridian', 'dim_customer') }}
