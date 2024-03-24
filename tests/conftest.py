import os
import pytest
import shutil
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

@pytest.fixture(params=["./dags/"])
def dag_bag(request):
    return DagBag(dag_folder=request.param, include_examples=False)