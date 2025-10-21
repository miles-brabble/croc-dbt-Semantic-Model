{{ config(materialized='table') }}

with dates as (
  select generate_series(
      '2010-01-01'::date,
      '2035-12-31'::date,
      interval '1 day'
  )::date as date
)
select date
from dates