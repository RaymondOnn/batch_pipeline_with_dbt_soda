FROM apache/airflow:slim-2.8.2-python3.11

HEALTHCHECK --interval=1m CMD curl -sLf http://localhost:8080/ || exit 1

# install airflow environment deps
RUN --mount=type=bind,source=src/docker/img.requirements.txt,target=/tmp/requirements.txt \
            pip install --no-cache-dir --user "apache-airflow==${AIRFLOW_VERSION}" --requirement /tmp/requirements.txt

# Set up dbt_venv
ENV PIP_USER=false
ENV VIRTUAL_ENV=/opt/airflow/dbt_venv
RUN python3 -m venv $VIRTUAL_ENV && ${VIRTUAL_ENV}/bin/pip install dbt-bigquery
ENV PIP_USER=true
