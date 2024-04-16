-- dim_datetime.sql

-- Create a CTE to extract date and time components
WITH dates_spine AS (
    SELECT dates AS date_key
    FROM (
        SELECT
            MIN(CAST(invoice_datetime AS DATE)) AS min_date,
            MAX(CAST(invoice_datetime AS DATE)) AS max_date
        FROM {{ ref('stg_invoices') }}
    ) AS t
    INNER JOIN UNNEST(GENERATE_DATE_ARRAY(t.min_date, t.max_date)) AS dates
),

dates_core AS (
    SELECT
        date_key,
        EXTRACT(YEAR FROM date_key) AS year,
        EXTRACT(QUARTER FROM date_key) AS quarter_num,
        EXTRACT(MONTH FROM date_key) AS month_num,
        EXTRACT(WEEK FROM date_key) AS week_num,
        EXTRACT(DAYOFWEEK FROM date_key) AS day_num_of_week,
        EXTRACT(DAYOFYEAR FROM date_key) AS day_num_of_year,
        FORMAT_DATE('%B', date_key) AS month_name_long
    FROM dates_spine
)

SELECT
    *,
    LEFT(month_name_long, 3) AS month_name_short,
    CONCAT('Q', quarter_num) AS quarter,
    IF(quarter_num IN (1, 2), 'H1', 'H2') AS half_year,
    CURRENT_TIMESTAMP() AS created_on,
    CURRENT_TIMESTAMP() AS last_updated
FROM dates_core
