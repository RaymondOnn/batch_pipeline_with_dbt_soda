# Reference: https://astronomer.github.io/astronomer-cosmos/getting_started/open-source.html  # noqa: E501
# Here, we define the ProfileConfig and ProjectConfig objects to be imported into the dag  # noqa: E501
from pathlib import Path

from cosmos.config import ProfileConfig
from cosmos.config import ProjectConfig

DBT_CONFIG = ProfileConfig(
    profile_name="online_retail",
    target_name="dev",
    profiles_yml_filepath=Path(
        "/opt/airflow/dags/online_retail/dbt/profiles.yml"
    ),  # noqa E501
)

DBT_PROJECT_CONFIG = ProjectConfig(
    dbt_project_path="/opt/airflow/dags/online_retail/dbt/",
)
