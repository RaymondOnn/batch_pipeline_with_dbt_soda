from datetime import timedelta

from airflow.utils.dates import days_ago

dag_default_args = {
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "start_date": days_ago(1),
    "catchup": False,
}
