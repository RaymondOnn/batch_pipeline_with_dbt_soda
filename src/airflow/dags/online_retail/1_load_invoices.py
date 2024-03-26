from airflow.decorators import dag
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)
from airflow.utils.dates import days_ago


GCP_CONN = "gcp"
GCS_BUCKET = "dbt_soda_online_retail"
GCS_DEST_PATH = "raw/online_retail.csv"
BQ_DATASET = "online_retail"
BQ_SRC_INVOICES = "raw_invoices"
SODA_IMG = "soda_checks"


@dag(
    start_date=days_ago(0),
    schedule=None,
    catchup=False,
)
def online_retail__01_load_invoices() -> None:

    start = EmptyOperator(task_id="start")

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_csv_to_gcs",
        src="/opt/airflow/dags/online_retail/dataset/online_retail.csv",
        dst=GCS_DEST_PATH,
        bucket=GCS_BUCKET,
        gcp_conn_id=GCP_CONN,
        mime_type="text/csv",
    )

    gcs_to_bq = GCSToBigQueryOperator(
        task_id="gcs_to_bq",
        gcp_conn_id=GCP_CONN,
        bucket=GCS_BUCKET,
        source_objects=[GCS_DEST_PATH],
        destination_project_dataset_table=f"{BQ_DATASET}.raw_invoices",
        create_disposition="CREATE_IF_NEEDED",  # create table if not exists
        write_disposition="WRITE_TRUNCATE",  # WRITE-APPEND/WRITE_EMPTY
        source_format="csv",
        skip_leading_rows=1,
        field_delimiter=",",
        autodetect=False,
        schema_fields=[
            {"name": "InvoiceNo", "type": "STRING", "mode": "NULLABLE"},
            {"name": "StockCode", "type": "STRING", "mode": "NULLABLE"},
            {"name": "Description", "type": "STRING", "mode": "NULLABLE"},
            {"name": "Quantity", "type": "INT64", "mode": "NULLABLE"},
            {"name": "InvoiceDate", "type": "STRING", "mode": "NULLABLE"},
            {"name": "UnitPrice", "type": "FLOAT64", "mode": "NULLABLE"},
            {"name": "CustomerID", "type": "STRING", "mode": "NULLABLE"},
            {"name": "Country", "type": "STRING", "mode": "NULLABLE"},
        ],
        encoding="ISO-8859-1",
    )

    check_invoices = DockerOperator(
        task_id="check_invoices",
        image=SODA_IMG,
        api_version="auto",
        docker_url="tcp://docker-proxy:2375",
        command="python run_checks.py check_invoices sources",
        auto_remove=True,
        mount_tmp_dir=False,
        # tty=True,
        network_mode="bridge",
    )

    end = EmptyOperator(task_id="end")

    chain(
        start,
        upload_csv_to_gcs,
        gcs_to_bq,
        check_invoices,
        end,
    )


online_retail__01_load_invoices()
