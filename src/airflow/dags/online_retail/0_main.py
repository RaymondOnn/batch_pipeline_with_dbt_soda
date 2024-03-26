from airflow.decorators import dag
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
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
def online_retail__00() -> None:

    start = EmptyOperator(task_id="start")

    start_load_invoices = TriggerDagRunOperator(
        task_id="trigger_load_invoices",
        trigger_dag_id="online_retail__01_load_invoices",
        wait_for_completion=True,
    )

    start_load_country = TriggerDagRunOperator(
        task_id="trigger_load_country",
        trigger_dag_id="online_retail__02_load_country",
        wait_for_completion=False,
    )

    start_staging = TriggerDagRunOperator(
        task_id="start_staging",
        trigger_dag_id="online_retail__03_staging",
        wait_for_completion=True,
    )

    start_transform = TriggerDagRunOperator(
        task_id="start_transform",
        trigger_dag_id="online_retail__04_transform",
        wait_for_completion=True,
    )

    start_report = TriggerDagRunOperator(
        task_id="start_report",
        trigger_dag_id="online_retail__05_report",
        wait_for_completion=True,
    )

    end = EmptyOperator(task_id="end")

    chain(
        start,
        [start_load_country, start_load_invoices],
        start_staging,
        start_transform,
        start_report,
        end,
    )


online_retail__00()
