-- Picking the right description based on which description is used more

WITH base AS (
    SELECT
        stock_code,
        product_desc,
        count(1) as n_desc,
    FROM {{ ref('stg_invoices') }}
    GROUP BY stock_code, product_desc
)
SELECT
    stock_code,
    product_desc,
FROM base
QUALIFY ROW_NUMBER() OVER(
    PARTITION BY stock_code
    ORDER BY n_desc DESC
) = 1
