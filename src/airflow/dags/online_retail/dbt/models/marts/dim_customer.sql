-- dim_customer.sql

-- Create the dimension table
WITH base AS (
    SELECT DISTINCT
        customer_key,
        customer_id,
        CASE
            WHEN country = 'EIRE' THEN 'Ireland'
            WHEN country = 'Unspecified' THEN 'Unknown'
            ELSE country
        END AS country
    FROM {{ ref('stg_invoices') }}
)

SELECT
    base.customer_id,
    base.country,
    CAST(base.customer_key AS STRING) AS customer_key,
    CAST(ctry.iso AS STRING) AS country_code,
    CURRENT_TIMESTAMP() AS created_on,
    CURRENT_TIMESTAMP() AS last_updated
FROM base
LEFT JOIN {{ source('online_retail', 'raw_country') }} AS ctry
    ON base.country = ctry.nicename
