-- dim_customer.sql

-- Create the dimension table
WITH customer_cte AS (
	SELECT DISTINCT
	    {{ dbt_utils.generate_surrogate_key(['CustomerID', 'Country']) }} as customer_id,
	    Country AS country
	FROM {{ source('online_retail', 'raw_invoices') }}
	WHERE CustomerID IS NOT NULL
)
SELECT
    cust.*,
	ctry.iso
FROM customer_cte cust
LEFT JOIN {{ source('online_retail', 'raw_country') }} ctry 
	ON cust.country = ctry.nicename