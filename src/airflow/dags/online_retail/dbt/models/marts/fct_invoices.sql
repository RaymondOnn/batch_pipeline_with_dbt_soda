-- fct_invoices.sql

-- Create the fact table by joining the relevant keys from dimension table
WITH fct_invoices_cte AS (
    SELECT
        InvoiceNo AS invoice_id,
        InvoiceDate AS datetime_id,
        {{ dbt_utils.generate_surrogate_key(['StockCode', 'Description', 'UnitPrice']) }} as product_id,
        {{ dbt_utils.generate_surrogate_key(['CustomerID', 'Country']) }} as customer_id,
        Quantity AS quantity,
        Quantity * UnitPrice AS total
    FROM {{ source('online_retail', 'raw_invoices') }}
    WHERE Quantity > 0
)
SELECT
    invoice_id,
    dt.datetime_id,
    prod.product_id,
    cust.customer_id,
    quantity,
    total
FROM fct_invoices_cte inv
INNER JOIN {{ ref('dim_date') }} dt ON inv.datetime_id = dt.datetime_id
INNER JOIN {{ ref('dim_product') }} prod ON inv.product_id = prod.product_id
INNER JOIN {{ ref('dim_customer') }} cust ON inv.customer_id = cust.customer_id
