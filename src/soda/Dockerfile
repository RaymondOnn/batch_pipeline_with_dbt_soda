FROM python:3.11-slim

WORKDIR /usr/src/app

RUN pip install soda-core-bigquery==3.2.3 soda-core-scientific==3.2.3  fire==0.6.0

COPY ./soda/ .
COPY ./dags/online_retail/gcp/ .

CMD ["python", "run_checks.py"]
