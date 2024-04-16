WITH agg AS (
    SELECT
        prod.product_key,
        prod.stock_code,
        SUM(inv.quantity) AS total_quantity_sold
    FROM (
        SELECT
            quantity,
            product_key
        FROM {{ ref('fct_invoices') }}
        WHERE is_non_sale = False
    ) AS inv
    LEFT JOIN {{ ref('dim_product') }} AS prod
        ON inv.product_key = prod.product_key
    GROUP BY prod.product_key, prod.stock_code
    ORDER BY total_quantity_sold DESC
)
SELECT
    agg.*,
    prod.product_desc
FROM agg
LEFT JOIN {{ ref('dim_product') }} AS prod ON agg.product_key = prod.product_key
