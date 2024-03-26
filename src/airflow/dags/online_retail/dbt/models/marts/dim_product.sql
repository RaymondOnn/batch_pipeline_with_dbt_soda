-- dim_product.sql
-- StockCode isn't unique, a product with the same id can have different and prices
-- Create the dimension table

With prices AS (
    SELECT DISTINCT
        product_key,
        stock_code,
        unit_price,
    FROM {{ ref('stg_invoices') }}

)
SELECT
    CAST(prices.product_key as STRING) as product_key,
    pdesc.stock_code,
    pdesc.product_desc,
    prices.unit_price,
    current_timestamp() as created_on,
    current_timestamp() as last_updated,
FROM {{ ref('stg_description') }} pdesc
LEFT JOIN prices ON prices.stock_code = pdesc.stock_code
