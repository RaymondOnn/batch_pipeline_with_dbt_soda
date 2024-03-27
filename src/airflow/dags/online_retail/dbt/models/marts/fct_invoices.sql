-- fct_invoices.sql

-- Create the fact table by joining the relevant keys from dimension table
SELECT
    invoice_id,
    quantity,
    is_cancelled,
    is_non_sale,
    CAST(product_key AS STRING) AS product_key,
    CAST(customer_key AS STRING) AS customer_key,
    EXTRACT(DATE FROM invoice_datetime) AS invoice_date,
    EXTRACT(TIME FROM invoice_datetime) AS invoice_time,
    CAST(quantity * unit_price AS NUMERIC) AS total_sales,
    CURRENT_TIMESTAMP() AS created_on,
    CURRENT_TIMESTAMP() AS last_updated
FROM {{ ref('stg_invoices') }}
