from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.config import ExecutionConfig
from cosmos.config import RenderConfig
from cosmos.constants import LoadMode
from online_retail.dbt.cosmos_config import DBT_CONFIG
from online_retail.dbt.cosmos_config import DBT_PROJECT_CONFIG
from online_retail.params import DBT_VENV_EXEC_PATH
from online_retail.params import DS_INVOICES_BQ
from online_retail.params import DS_STAGING_BQ

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

# from airflow.models.connection import Connection


@dag(
    start_date=days_ago(0),
    schedule=[DS_INVOICES_BQ],
    catchup=False,
)
def online_retail__03_staging() -> None:

    start = EmptyOperator(task_id="start")

    dbt_stg = DbtTaskGroup(
        group_id="dbt_stg",
        profile_config=DBT_CONFIG,
        project_config=DBT_PROJECT_CONFIG,
        render_config=RenderConfig(  # controls how task are rendered visually
            load_method=LoadMode.DBT_LS, select=["path:models/staging"]
        ),
        execution_config=ExecutionConfig(
            dbt_executable_path=DBT_VENV_EXEC_PATH,
        ),
    )

    end = EmptyOperator(
        task_id="end",
        outlets=[DS_STAGING_BQ],
    )

    dbt_stg.set_upstream(start)
    dbt_stg.set_downstream(end)


online_retail__03_staging()
