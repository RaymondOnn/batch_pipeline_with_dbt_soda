-- report_year_invoices.sql
SELECT
  dt.year,
  dt.month,
  COUNT(DISTINCT inv.invoice_id) AS num_invoices,
  SUM(inv.total) AS total_revenue
FROM {{ ref('fct_invoices') }} inv
JOIN {{ ref('dim_date') }} dt ON inv.datetime_id = dt.datetime_id
GROUP BY dt.year, dt.month
ORDER BY dt.year, dt.month