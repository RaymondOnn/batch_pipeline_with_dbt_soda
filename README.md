# Data marts with `dbt` and `soda`

An end-to-end pipeline that extract data from `.csv` files and transforms it to create data models for analytics use cases

### Project Objective
- Implement new tools i.e. dbt, soda, astronomer-cosmos, metabase
- Set up automated testing (using Github actions)

### Architecture
![alt text](images/architecture.png)

### Workflow

``` mermaid
sequenceDiagram
    autonumber
    par Airflow to Csv File
        Airflow ->> Csv File: Triggers task
    and Airflow to BigQuery
        Airflow ->> BigQuery: Triggers task
    end
    BigQuery->>raw_country table: Check if exists
    alt if not exists
        BigQuery->>raw_country table: Creates table and run INSERT job
    end
    Csv File ->> Cloud Storage: Upload File
    Cloud Storage ->> BigQuery: Loads data
    Note over BigQuery: raw_invoices created
    BigQuery ->> soda-core: Checks data
    soda-core ->> dbt: Transform data
    Note over dbt: stg_invoices, stg_description created
    dbt ->> dbt: Transform data
    Note over dbt: Dim and Fact tables created
    dbt ->> soda-core: Checks data
    soda-core ->> dbt: Transform data
    Note over dbt: Report tables created
    dbt ->> soda-core: Checks data
```

### Data Model
![alt text](images/ERD.svg)


### Lessons Learnt
- DagBag import error
- . is a path relative to the docker-compose file

## Running the project

### Prerequisites
To run the pipeline you'll need:
  - Docker
  - Google Cloud Platform's`service_account.json` (credentials needed to use Bigquery and Cloud Storage)

### Steps required
1. Clone the repo
  ``` sh
  git clone <GIT_REPO_URL>
  ```
1. Change the working directory to the folder containing the file contents
  ``` sh
  cd <FOLDER_NAME>
  ```

1. Swapping credentials
- Place your `service_account.json` file under `./src/airflow/dags/online_retail/gcp/`
- Update the `project_id` value.
  - Copy and paste the `project_id` value from your `service_account.json`
  - Do this for these files:
    - `./src/soda/configuration.yml`
    - `./src/airflow/dags/online_retail/dbt/profiles.yml`

1. Start the Docker containers
   - if you have `make` installed
    ```yaml
    make start
    ```
  - Otherwise, use this command instead
    ```
    docker compose -f ./docker-compose.yaml -f ./src/docker/docker-compose.viz.yaml up -d
    ```
  - Once the container have started,
    - Airflow UI will be accessible via http://localhost:8080.
    - Metabase will be accessible via http://localhost:3000

2. Log into Airflow using `airflow` as the user and password
3. To see the pipeline work, trigger on the dag `01_load_invoices`.
   - This dag will trigger the rest of the dags that make up the pipeline
