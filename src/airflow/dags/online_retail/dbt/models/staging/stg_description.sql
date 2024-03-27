-- Picking the right description based on which description is used more

WITH base AS (
    SELECT
        stock_code,
        product_desc,
        count(*) AS n_desc
    FROM {{ ref('stg_invoices') }}
    WHERE is_non_sale = False
    GROUP BY stock_code, product_desc
)

SELECT
    stock_code,
    product_desc
FROM base
QUALIFY row_number() OVER (
    PARTITION BY stock_code
    ORDER BY n_desc DESC
) = 1
