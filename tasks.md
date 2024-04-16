# Enhancements
- testing: <https://stackoverflow.com/questions/73612210/apache-airflow-unit-and-integration-test>
- Slack alert on failure: <https://towardsdatascience.com/automated-alerts-for-airflow-with-slack-5c6ec766a823>
- monitoring: <https://www.youtube.com/watch?v=xyeR_uFhnD4>
- Reduce size of image: <https://pythonspeed.com/articles/multi-stage-docker-python>
- schema evolution:
- data contract:
``` py
import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel

class DagDefinition(BaseModel):
    default_schedule_time:str
    start_date: datetime.datetime
    dag_frequency: Literal['daily','hourly']
    description: Optional[str]
    task_concurrency:Optional[int]
    max_active_dag_runs:Optional[int]
    data_points:List[DataPoints]
```
- switch airflow to cloud composer. Use terraform to provision resources
