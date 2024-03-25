# Reference: https://astronomer.github.io/astronomer-cosmos/getting_started/open-source.html
# Here, we define the ProfileConfig and ProjectConfig objects to be imported into the dag

from cosmos.config import ProfileConfig, ProjectConfig
from pathlib import Path

DBT_CONFIG = ProfileConfig(
    profile_name='online_retail',
    target_name='dev',
    profiles_yml_filepath=Path('/opt/airflow/dags/online_retail/dbt/profiles.yml')
)

DBT_PROJECT_CONFIG=ProjectConfig(
    dbt_project_path='/opt/airflow/dags/online_retail/dbt/',
)
