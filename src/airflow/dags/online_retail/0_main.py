from common.defaults import dag_default_args
from online_retail.params import DS_START

from airflow.decorators import dag
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator


@dag(
    default_args=dag_default_args,
    schedule=None,
)
def online_retail__00() -> None:

    start = EmptyOperator(task_id="start")

    start_pipeline = EmptyOperator(
        task_id="start_pipeline",
        outlets=[DS_START],
    )
    # start_load_invoices = TriggerDagRunOperator(
    #     task_id="trigger_load_invoices",
    #     trigger_dag_id="online_retail__01_load_invoices",
    #     wait_for_completion=True,
    # )

    # start_load_country = TriggerDagRunOperator(
    #     task_id="trigger_load_country",
    #     trigger_dag_id="online_retail__02_load_country",
    #     wait_for_completion=False,
    # )

    # start_staging = TriggerDagRunOperator(
    #     task_id="start_staging",
    #     trigger_dag_id="online_retail__03_staging",
    #     wait_for_completion=True,
    # )

    # start_transform = TriggerDagRunOperator(
    #     task_id="start_transform",
    #     trigger_dag_id="online_retail__04_transform",
    #     wait_for_completion=True,
    # )

    # start_report = TriggerDagRunOperator(
    #     task_id="start_report",
    #     trigger_dag_id="online_retail__05_report",
    #     wait_for_completion=True,
    # )

    end = EmptyOperator(task_id="end")

    # [start_load_country, start_load_invoices],
    # start_staging,
    # start_transform,
    # start_report,
    chain(
        start,
        start_pipeline,
        end,
    )


online_retail__00()
