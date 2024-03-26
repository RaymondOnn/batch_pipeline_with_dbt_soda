-- report_year_invoices.sql
SELECT
  dt.year,
  dt.month_num,
  COUNT(DISTINCT inv.invoice_id) AS num_invoices,
  SUM(inv.total_sales) AS total_revenue
FROM {{ ref('fct_invoices') }} inv
JOIN {{ ref('dim_date') }} dt ON inv.invoice_date = dt.date_key
GROUP BY dt.year, dt.month_num
ORDER BY dt.year, dt.month_num
