WITH base AS (
    SELECT
        CAST(invoiceno AS STRING) AS invoice_id,
        UPPER(CAST(stockcode AS STRING)) AS stock_code,
        CAST(description AS STRING) AS product_desc,
        CAST(quantity AS INTEGER) AS quantity,
        PARSE_DATETIME('%m/%d/%y %H:%M', invoicedate) AS invoice_datetime,
        CAST(unitprice AS NUMERIC) AS unit_price,
        CAST(customerid AS INTEGER) AS customer_id,
        CAST(country AS STRING) AS country
    FROM {{ source('online_retail', 'raw_invoices') }}
    WHERE TRUE
        AND UnitPrice > 0
        AND Quantity > 0
)
SELECT
    *,
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'country']) }} AS customer_key,
    {{ dbt_utils.generate_surrogate_key(['stock_code', 'unit_price']) }} AS product_key,
    CASE
        WHEN STARTS_WITH(invoice_id, 'C') THEN True
        ELSE False
    END AS is_cancelled,
    CASE
        WHEN REGEXP_CONTAINS(stock_code, '[0-9]{5}.*') THEN False
        ELSE True
    END AS is_non_sale,
FROM base
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY invoice_id, stock_code, quantity, unit_price
    ORDER BY invoice_id, stock_code, quantity, unit_price
) = 1
