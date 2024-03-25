-- report_customer_invoices.sql
SELECT
  cust.country,
  cust.iso,
  COUNT(inv.invoice_id) AS total_invoices,
  SUM(inv.total) AS total_revenue
FROM {{ ref('fct_invoices') }} inv
JOIN {{ ref('dim_customer') }} cust ON inv.customer_id = cust.customer_id
GROUP BY cust.country, cust.iso
ORDER BY total_revenue DESC
LIMIT 10
