from airflow import Dataset

GCP_CONN = "gcp"
GCS_BUCKET = "dbt_soda_online_retail"
GCS_DEST_PATH = "raw/online_retail.csv"
BQ_DATASET = "online_retail"
BQ_SRC_INVOICES = "raw_invoices"
BQ_SRC_COUNTRY = "raw_country"
SODA_IMG = "soda_checks"
DBT_VENV_EXEC_PATH = "/opt/airflow/dbt_venv/bin/dbt"


# Datasets
DS_START = Dataset("start")
DS_INVOICES_BQ = Dataset(f"{BQ_DATASET}.{BQ_SRC_INVOICES}")
DS_COUNTRY_BQ = Dataset(f"{BQ_DATASET}.{BQ_SRC_COUNTRY}")
DS_STAGING_BQ = Dataset(f"{BQ_DATASET}.stg_invoices")
DS_TRANSFORM_BQ = Dataset(f"{BQ_DATASET}.fct_invoices")
