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
		END AS country,
	FROM {{ ref('stg_invoices') }}
)
SELECT
	CAST(base.customer_key as STRING) AS customer_key,
    base.customer_id,
	base.country,
	CAST(ctry.iso as STRING) AS country_code,
	current_timestamp() as created_on,
    current_timestamp() as last_updated,
FROM base
LEFT JOIN {{ source('online_retail', 'raw_country') }} ctry
	ON base.country = ctry.nicename
