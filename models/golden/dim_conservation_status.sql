{{ config(materialized='view') }}

select
 *
from {{ source('GOLDEN','dim_conservation_status') }}