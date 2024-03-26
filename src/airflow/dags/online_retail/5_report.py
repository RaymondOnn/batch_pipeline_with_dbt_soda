from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.config import ExecutionConfig
from cosmos.config import RenderConfig
from cosmos.constants import LoadMode
from online_retail.dbt.cosmos_config import DBT_CONFIG
from online_retail.dbt.cosmos_config import DBT_PROJECT_CONFIG

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

# from airflow.models.connection import Connection


BQ_DATASET = "online_retail"
SODA_IMG = "soda_checks"
DBT_VENV_EXEC_PATH = "/opt/airflow/dbt_venv/bin/dbt"


@dag(
    start_date=days_ago(0),
    schedule=None,
    catchup=False,
)
def online_retail__05_report() -> None:

    start = EmptyOperator(task_id="start")

    dbt_reports = DbtTaskGroup(
        group_id="dbt_reports",
        profile_config=DBT_CONFIG,
        project_config=DBT_PROJECT_CONFIG,
        render_config=RenderConfig(  # controls how task are rendered visually
            load_method=LoadMode.DBT_LS, select=["path:models/reports"]
        ),
        execution_config=ExecutionConfig(
            dbt_executable_path=DBT_VENV_EXEC_PATH,
        ),
    )

    check_reports = DockerOperator(
        task_id="check_reports",
        image=SODA_IMG,
        api_version="auto",
        docker_url="tcp://docker-proxy:2375",
        command="python run_checks.py check_reports reports",
        auto_remove=True,
        mount_tmp_dir=False,
        # tty=True,
        network_mode="bridge",
    )

    end = EmptyOperator(task_id="end")

    dbt_reports.set_upstream(start)
    dbt_reports.set_downstream(check_reports)
    check_reports.set_downstream(end)


online_retail__05_report()
