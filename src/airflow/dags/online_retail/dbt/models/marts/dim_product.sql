-- dim_product.sql
-- StockCode isn't unique, a product with the same id can have different and prices
-- Create the dimension table

With prices As (
    Select Distinct
        product_key,
        stock_code,
        unit_price
    From {{ ref('stg_invoices') }}

)

Select
    pdesc.stock_code,
    pdesc.product_desc,
    prices.unit_price,
    CAST(prices.product_key As STRING) As product_key,
    CURRENT_TIMESTAMP() As created_on,
    CURRENT_TIMESTAMP() As last_updated
From {{ ref('stg_description') }} As pdesc
Left Join prices On pdesc.stock_code = prices.stock_code
