from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.config import ExecutionConfig
from cosmos.config import RenderConfig
from cosmos.constants import LoadMode
from online_retail.dbt.cosmos_config import DBT_CONFIG
from online_retail.dbt.cosmos_config import DBT_PROJECT_CONFIG
from online_retail.params import DBT_VENV_EXEC_PATH
from online_retail.params import DS_COUNTRY_BQ
from online_retail.params import DS_STAGING_BQ
from online_retail.params import DS_TRANSFORM_BQ
from online_retail.params import SODA_IMG

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago


@dag(
    start_date=days_ago(0),
    schedule=[DS_STAGING_BQ, DS_COUNTRY_BQ],
    catchup=False,
)
def online_retail__04_transform() -> None:

    start = EmptyOperator(task_id="start")

    # DbtTaskGroup is a custom TaskGroup from Cosmos
    # Info regarding configs: https://astronomer.github.io/astronomer-cosmos/configuration/render-config.html # noqa: E501
    dbt_marts = DbtTaskGroup(
        group_id="dbt_marts",
        profile_config=DBT_CONFIG,
        project_config=DBT_PROJECT_CONFIG,
        render_config=RenderConfig(  # controls how task are rendered visually
            load_method=LoadMode.DBT_LS,
            select=["path:models/marts"],
        ),
        execution_config=ExecutionConfig(
            dbt_executable_path=DBT_VENV_EXEC_PATH,
        ),
    )

    check_marts = DockerOperator(
        task_id="check_marts",
        image=SODA_IMG,
        api_version="auto",
        docker_url="tcp://docker-proxy:2375",
        command="python run_checks.py check_marts marts",
        auto_remove=True,
        mount_tmp_dir=False,
        # tty=True,
        network_mode="bridge",
        outlets=[DS_TRANSFORM_BQ],
    )

    end = EmptyOperator(
        task_id="end",
    )

    start >> dbt_marts >> check_marts >> end


online_retail__04_transform()
