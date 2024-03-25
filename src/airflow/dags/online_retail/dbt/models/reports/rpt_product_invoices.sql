-- report_product_invoices.sql
SELECT
  prod.product_id,
  prod.stock_code,
  prod.description,
  SUM(inv.quantity) AS total_quantity_sold
FROM {{ ref('fct_invoices') }} inv
JOIN {{ ref('dim_product') }} prod ON inv.product_id = prod.product_id
GROUP BY prod.product_id, prod.stock_code, prod.description
ORDER BY total_quantity_sold DESC
LIMIT 10
