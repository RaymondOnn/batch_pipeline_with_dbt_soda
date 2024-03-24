FROM apache/airflow:slim-2.8.2-python3.11

# install airflow environment deps
# ADD docker/img.requirements.txt docker/run_tests.py ./
# RUN pip install apache-airflow==${AIRFLOW_VERSION} -r img.requirements.txt
#ADD src/docker/run_tests.py .
RUN --mount=type=bind,source=src/docker/img.requirements.txt,target=/tmp/requirements.txt \
            pip install --user apache-airflow==${AIRFLOW_VERSION} --requirement /tmp/requirements.txt

# Set up dbt_venv
ENV PIP_USER=false
ENV VIRTUAL_ENV=/opt/airflow/dbt_venv
RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN ${VIRTUAL_ENV}/bin/pip install dbt-bigquery
ENV PIP_USER=true
