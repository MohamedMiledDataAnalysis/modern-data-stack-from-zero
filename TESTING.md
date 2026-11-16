# How the book was tested

Every command, script and expected output in *The Modern Data Stack* (Second Edition) was run before
publication, except where this table says otherwise. Versions are those pinned in `requirements.txt`
and in each chapter's folder, as of November 2026.

**Where:** *Local* = run on a Linux machine with Python 3.13 and PostgreSQL 16.
*GitHub Actions* = run by the workflow named, on GitHub's Ubuntu 24.04 servers, for tools that need
Docker images or Maven/CRAN downloads.

| Ch | Tool | Executed | Where | Not executed |
|---:|:--|:--|:--|:--|
| 0 | Setup | `check_setup.py` | Local | Installers on Windows and macOS |
| 1 | PostgreSQL | all queries, exercises | Local | — |
| 2 | Files, APIs, IoT | all scripts, mock API, MQTT simulator | Local | — |
| 3 | NiFi 2.12.0 | start-up | `ch03-nifi.yml` | the canvas steps (clicks) |
| 4 | Kafka 4.4.0 | producer, consumer, exercises | `ch04-kafka.yml` | — |
| 5 | Airbyte 2.5.0 | install with abctl, source, destination, full and incremental syncs (through the API) | `ch05-airbyte.yml` | the same steps clicked in the web interface |
| 6 | Fivetran | `simulate_destination.sql`, `queries.sql`, MAR estimate | Local | everything inside Fivetran's service |
| 7 | Stitch / Singer | Singer tap and target, exercises | Local | everything inside Stitch's service |
| 8 | Amazon S3 | all scripts against moto | Local | real AWS account |
| 9 | Cloud Storage | all scripts against fake-gcs-server 1.52 | `ch09-gcs.yml` | lifecycle rules and location on real Google Cloud |
| 10 | Snowflake | load, queries, clone, exercises 1–2 against fakesnow 0.12.1 | Local | Time Travel, resource monitor, Exercise 3, real account |
| 11 | BigQuery | load and Step 3–4 query against bigquery-emulator 0.8.1, first quarter of 2023 | `ch11-bigquery.yml` | exercise GoogleSQL (answers from `check_exercises.sql` in PostgreSQL); real sandbox |
| 12 | Microsoft Fabric | Parquet export; notebook code on local Spark; all T-SQL on SQL Server 2022 | Local, `ch12-tsql.yml` | everything inside Fabric |
| 13 | Spark 4.2.0 | all scripts, exercises | Local | — |
| 14 | dbt 1.12.7 | models, tests, exercises | Local | — |
| 15 | Delta Lake 4.4.1 | Part A, exercises | `ch15-delta.yml` | Part B on Databricks Free Edition |
| 16 | Beam 2.77.0 | batch and streaming pipelines, exercises | Local | — |
| 17 | pandas 3.1.1 | all scripts, exercises | Local | — |
| 18 | Python analysis | all scripts, exercises | Local | — |
| 19 | R 4.6.2 | `analysis.R`, exercises | `ch19-r.yml` | — |
| 20 | Jupyter | notebook, papermill runs, exercises | Local | — |
| 21 | scikit-learn 1.9.1 | all scripts, exercises | Local | — |
| 22 | statsmodels 0.15.0 | all scripts, exercises | Local | — |
| 23 | Tableau | Hyper extract; every view's figure in SQL | Local | the clicks in Tableau Desktop |
| 24 | Power BI | every visual's figure in PostgreSQL | Local | the DAX itself, in Power BI |
| 25 | Looker Studio | CSV export; every chart's figure in PostgreSQL | Local | the clicks in Looker Studio |
| 26 | Superset 6.1.0 | start-up, connection, dataset, SQL Lab, chart, exercises (through the API) | `ch26-superset.yml` | the same steps clicked in the web interface |
| 27 | Excel | report built with openpyxl, values checked | Local | opening the file in Excel |
| 28 | Streamlit 1.67.0 | app and AppTest tests | Local | — |
| 29 | FastAPI 0.163.1 | API and tests | Local | — |
| 30 | Flask 3.1.3 | app, exercises | Local | — |
| 31 | R Shiny 1.14.0 | server tests | `ch31-shiny.yml` | — |
| 32 | Great Expectations 1.25.0 | suites, checkpoint, quality gate | Local | — |
| 33 | Airflow 3.4.0 | install with constraints; DAG runs | `ch33-airflow-install.yml`, Local | — |
| 34 | Prometheus 3.16.0 | exporter, scraping, alert rules, PromQL | `ch34-35-monitoring.yml` | — |
| 35 | Grafana 13.3.1 | provisioned data source and dashboard | `ch34-35-monitoring.yml` | — |

Steps marked "not executed" were written from the vendors' documentation of November 2026. Web
interfaces change several times a year; the chapters name each screen and field so that a moved
button can be found by its label.
