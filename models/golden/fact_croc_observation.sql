{{ config(materialized='view') }}

select
 *
from {{ source('GOLDEN','fact_croc_observation') }}