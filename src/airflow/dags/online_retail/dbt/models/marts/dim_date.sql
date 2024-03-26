-- dim_datetime.sql

-- Create a CTE to extract date and time components
WITH dates_spine AS (
  SELECT dates as date_key
  FROM (
    SELECT
      MIN(CAST(invoice_datetime AS DATE)) as min_date,
      MAX(CAST(invoice_datetime AS DATE)) as max_date
    FROM {{ ref('stg_invoices') }}
  ) t
  INNER JOIN UNNEST(GENERATE_DATE_ARRAY(t.min_date, t.max_date)) dates
),
dates_core as (
  SELECT
    date_key,
    EXTRACT(year FROM date_key) as year,
    EXTRACT(quarter FROM date_key) as quarter_num,
    EXTRACT(month FROM date_key) as month_num,
    EXTRACT(week FROM date_key) as week_num,
    EXTRACT(dayofweek FROM date_key) as day_num_of_week,
    EXTRACT(dayofyear  FROM date_key) as day_num_of_year,
    FORMAT_DATE('%B',date_key) as month_name_long,
    FROM dates_spine
)
SELECT
  *,
  LEFT(month_name_long, 3) AS month_name_short,
  CONCAT('Q', quarter_num) AS quarter,
  IF(quarter_num in(1,2), 'H1', 'H2') AS half_year,
  current_timestamp() as created_on,
  current_timestamp() as last_updated,
from dates_core
