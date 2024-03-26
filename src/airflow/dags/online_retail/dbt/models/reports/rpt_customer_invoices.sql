-- report_customer_invoices.sql
SELECT
  cust.country,
  cust.country_code,
  COUNT(inv.invoice_id) AS total_invoices,
  SUM(inv.total_sales) AS total_revenue
FROM {{ ref('fct_invoices') }} inv
JOIN {{ ref('dim_customer') }} cust ON inv.customer_key = cust.customer_key
GROUP BY cust.country, cust.country_code
ORDER BY total_revenue DESC
