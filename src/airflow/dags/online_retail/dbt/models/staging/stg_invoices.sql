WITH base AS (
    SELECT
        CAST(InvoiceNo AS STRING) as invoice_id,
        UPPER(CAST(StockCode as STRING)) as stock_code,
        CAST(Description as STRING) as product_desc,
        CAST(Quantity as INTEGER) as quantity,
        PARSE_DATETIME('%m/%d/%y %H:%M', InvoiceDate) AS invoice_datetime,
        CAST(UnitPrice as NUMERIC) as unit_price,
        CAST(CustomerID as INTEGER) as customer_id,
        CAST(Country AS STRING) as country
    FROM {{ source('online_retail', 'raw_invoices') }}
    WHERE TRUE
        AND UnitPrice > 0
        AND Quantity > 0
)
SELECT
    *,
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'country']) }} as customer_key,
    {{ dbt_utils.generate_surrogate_key(['stock_code', 'unit_price']) }} as product_key,
    CASE
        WHEN STARTS_WITH(invoice_id, 'C') THEN True
        ELSE False
    END as is_cancelled,
    CASE
        WHEN REGEXP_CONTAINS(stock_code, '[0-9]{5}.*') THEN False
        ELSE True
    END as is_non_sale,
FROM base
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY invoice_id, stock_code, quantity, unit_price
    ORDER BY invoice_id, stock_code, quantity, unit_price
) = 1
