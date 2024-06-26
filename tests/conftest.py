import logging
import os
from contextlib import contextmanager

import pytest

from airflow.models import DagBag

os.environ["AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS"] = "False"
os.environ["AIRFLOW__CORE__LOAD_EXAMPLES"] = "False"
os.environ["AIRFLOW__CORE__INIT_TEST_MODE"] = "True"
os.environ["AIRFLOW__HOME"] = os.path.dirname(os.path.dirname(__file__))
print(os.environ["AIRFLOW__HOME"])

# @pytest.fixture(autouse=True, scope="session")
# def reset_db():
#     from airflow.utils import db

#     db.resetdb()
#     yield

# os.remove(os.path.join(os.environ["AIRFLOW_HOME"], "unittests.cfg"))
# os.remove(os.path.join(os.environ["AIRFLOW_HOME"], "unittests.db"))
# os.remove(os.path.join(os.environ["AIRFLOW_HOME"], "webserver_config.py"))
# shutil.rmtree(os.path.join(os.environ["AIRFLOW_HOME"], "logs"))


@contextmanager
def suppress_logging(namespace):
    logger = logging.getLogger(namespace)
    old_value = logger.disabled
    logger.disabled = True
    try:
        yield
    finally:
        logger.disabled = old_value


@pytest.fixture(params=["./dags/"])
def dag_bag(request):
    with suppress_logging("airflow"):
        return DagBag(dag_folder=request.param, include_examples=False)
