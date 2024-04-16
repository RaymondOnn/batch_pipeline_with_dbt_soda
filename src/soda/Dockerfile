FROM python:3.11-slim

WORKDIR /usr/src/app

RUN pip install --no-cache-dir soda-core-bigquery==3.2.3 soda-core-scientific==3.2.3  fire==0.6.0

COPY ./src/soda/ .
COPY ./src/airflow/dags/online_retail/gcp/service_account.json .

CMD ["python", "run_checks.py"]
