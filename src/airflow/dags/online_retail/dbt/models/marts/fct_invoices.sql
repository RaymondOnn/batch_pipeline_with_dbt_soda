-- fct_invoices.sql

-- Create the fact table by joining the relevant keys from dimension table
SELECT
    invoice_id,
    CAST(product_key AS STRING) AS product_key,
    CAST(customer_key AS STRING) AS customer_key,
    EXTRACT(date FROM invoice_datetime) as invoice_date,
    EXTRACT(time FROM invoice_datetime) as invoice_time,
    quantity,
    CAST(quantity * unit_price AS NUMERIC) AS total_sales,
    CASE
        WHEN STARTS_WITH(invoice_id, 'C') THEN True
        ELSE False
    END as is_cancelled,
    current_timestamp() as created_on,
    current_timestamp() as last_updated,
FROM {{ ref('stg_invoices') }}
