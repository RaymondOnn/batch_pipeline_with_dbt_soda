from common.defaults import dag_default_args
from online_retail.params import BQ_DATASET
from online_retail.params import DS_INVOICES_BQ
from online_retail.params import DS_START
from online_retail.params import GCP_CONN
from online_retail.params import GCS_BUCKET
from online_retail.params import GCS_DEST_PATH
from online_retail.params import SODA_IMG

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


@dag(
    default_args=dag_default_args,
    schedule=[DS_START],  # None
    catchup=dag_default_args["catchup"],
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

    end = EmptyOperator(
        task_id="end",
        outlets=[DS_INVOICES_BQ],
    )

    chain(
        start,
        upload_csv_to_gcs,
        gcs_to_bq,
        check_invoices,
        end,
    )


online_retail__01_load_invoices()
