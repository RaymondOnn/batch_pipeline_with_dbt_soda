from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyTableOperator,
)
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryInsertJobOperator,
)  # noqa: E501
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryValueCheckOperator,
)  # noqa: E501
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

GCP_CONN = "gcp"
BQ_DATASET = "online_retail"
BQ_SRC_COUNTRY = "raw_country"


@dag(
    start_date=days_ago(0),
    schedule=None,
    catchup=False,
)
def online_retail__02_load_country() -> None:
    start = EmptyOperator(task_id="start")

    check_table_exists = BigQueryValueCheckOperator(
        task_id="check_table_exists",
        sql=f"""
            SELECT COUNT(1)
            FROM {BQ_DATASET}.INFORMATION_SCHEMA.TABLES
            WHERE table_name='{BQ_SRC_COUNTRY}';
        """,
        pass_value=1,  # table exists
        use_legacy_sql=False,
        gcp_conn_id=GCP_CONN,
        location="US",
    )

    create_country_table = BigQueryCreateEmptyTableOperator(
        task_id="create_country_table",
        trigger_rule=TriggerRule.ALL_FAILED,
        dataset_id=BQ_DATASET,
        table_id=BQ_SRC_COUNTRY,
        gcp_conn_id=GCP_CONN,
        if_exists="ignore",
        schema_fields=[
            {"name": "id", "type": "INT64", "mode": "REQUIRED"},
            {"name": "iso", "type": "STRING", "mode": "REQUIRED"},
            {"name": "name", "type": "STRING", "mode": "REQUIRED"},
            {"name": "nicename", "type": "STRING", "mode": "REQUIRED"},
            {"name": "iso3", "type": "STRING", "mode": "NULLABLE"},
            {"name": "numcode", "type": "INT64", "mode": "NULLABLE"},
            {"name": "phonecode", "type": "INT64", "mode": "REQUIRED"},
        ],
    )

    insert_country_info = BigQueryInsertJobOperator(
        task_id="insert_country_info",
        gcp_conn_id=GCP_CONN,
        configuration={
            "query": {
                "query": "{% include 'gcp/raw_country.sql' %}",
                "useLegacySql": False,
            }
        },
        location="US",
    )

    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.ONE_SUCCESS)

    (
        start
        >> check_table_exists
        >> create_country_table
        >> insert_country_info
        >> end
    )  # noqa: E501
    check_table_exists >> end


online_retail__02_load_country()
