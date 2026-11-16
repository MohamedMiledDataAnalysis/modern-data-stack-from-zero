# How the book was tested

Every command, script and expected output in *The Modern Data Stack* (Second Edition) was run before
publication, except where this table says otherwise. Versions are those pinned in `requirements.txt`
and in each chapter's folder, as of November 2026.

**Where:** *Local* = run on a Linux machine with Python 3.13 and PostgreSQL 16.
A workflow name = run on GitHub's servers by that file in `.github/workflows/`.

## The reader's run: `reproduce.yml`

On every push, `reproduce.yml` does what a reader does, on a clean Ubuntu 24.04 machine (the
system Windows readers use through WSL) and on a clean macOS 15 machine (Apple Silicon):
installs Python 3.13, Java 21 and PostgreSQL 16, creates the database user with Chapter 1's
script, creates the virtual environment, runs `pip install -r requirements.txt`, generates
Meridian, then runs every chapter's scripts and corrections in book order, including the
separate environments of Chapters 10, 16 and 33. Chapters that need Docker (3, 4, 5, 9, 11,
12's SQL Server, 26, 34, 35) or R (19, 31) run in their own workflows, on Ubuntu.

## Chapter by chapter

| Ch | Tool | Executed | Where | Not executed |
|---:|:--|:--|:--|:--|
| 0 | Setup | `check_setup.py` | Local, `reproduce.yml` | Installers on Windows and macOS |
| 1 | PostgreSQL | all queries, exercises | Local, `reproduce.yml` | — |
| Interlude | SQL dialects | the five queries in `sql-dialects/` | PostgreSQL 16 and Spark SQL: Local, `reproduce.yml`; Snowflake SQL on fakesnow: Local, `reproduce.yml`; T-SQL on SQL Server 2022: `ch12-tsql.yml`; GoogleSQL on the BigQuery emulator: `ch11-bigquery.yml` | query 4 on the BigQuery emulator returns 0 for the running total, an emulator fault; the other 24 results match |
| 2 | Files, APIs, IoT, SQL Server 2022 | all scripts, mock API, MQTT simulator; SQL Server source (`sqlserver/`) and Exercise 6 | Local, `reproduce.yml` (SQL Server and MQTT on the Ubuntu runner) | SQL Server on macOS was not run: GitHub's macOS runner has no Docker |
| 3 | NiFi 2.12.0 | start-up; the flow of Steps 3–7 built with the same settings through the REST API, 500 valid / 3 rejected | `ch03-nifi.yml` | the canvas clicks themselves; provenance screens |
| 4 | Kafka 4.4.0 | producer, consumer, exercises | `ch04-kafka.yml` | — |
| 5 | Airbyte 2.5.0 | install with abctl, source, destination, full and incremental syncs (through the API) | `ch05-airbyte.yml` | the same steps clicked in the web interface |
| 6 | Fivetran | `simulate_destination.sql`, `queries.sql`, MAR estimate | Local, `reproduce.yml` | everything inside Fivetran's service |
| 7 | Stitch / Singer | Singer tap and target, exercises | Local, `reproduce.yml` | everything inside Stitch's service |
| 8 | Amazon S3 | all scripts against moto | Local, `reproduce.yml` | real AWS account |
| 9 | Cloud Storage | all scripts against fake-gcs-server 1.52 | `ch09-gcs.yml` | lifecycle rules and location on real Google Cloud |
| 10 | Snowflake | load, queries, clone, exercises 1–2 against fakesnow 0.12.1, in the chapter's own environment | Local, `reproduce.yml` | Time Travel, resource monitor, Exercise 3, real account |
| 11 | BigQuery | load and Step 3–4 query against bigquery-emulator 0.8.1, first quarter of 2023 | `ch11-bigquery.yml` | exercise GoogleSQL (answers from `check_exercises.sql` in PostgreSQL); real sandbox |
| 12 | Microsoft Fabric | Parquet export; notebook code on local Spark; all T-SQL on SQL Server 2022 | Local, `ch12-tsql.yml`, `reproduce.yml` | everything inside Fabric |
| 13 | Spark 4.2.0 | all scripts, exercises | Local, `reproduce.yml` | — |
| 14 | dbt 1.12.7 | models, tests, exercises | Local, `reproduce.yml` | — |
| 15 | Delta Lake 4.4.1 | Part A, exercises; `export_for_databricks.py` | `ch15-delta.yml`, `reproduce.yml` | Part B on Databricks Free Edition |
| 16 | Beam 2.77.0 | batch and streaming pipelines, exercises | Local, `reproduce.yml` | Step 5 on Google Cloud Dataflow |
| 17 | pandas 3.1.1 | all scripts, exercises; Step 7 (`scale_up.py`, `size_test.py`) at 5 and 20 million orders | Local, `reproduce.yml` | every-column pandas on 20 million orders runs on the 16 GB Ubuntu runner only; on 8 GB it is stopped (`Killed`), as the book shows |
| 18 | Python analysis | all scripts, exercises | Local, `reproduce.yml` | — |
| 19 | R 4.6.2 | `analysis.R`, exercises | `ch19-r.yml` | — |
| 20 | Jupyter | notebook, papermill runs, exercises | Local, `reproduce.yml` | — |
| 21 | scikit-learn 1.9.1 | all scripts, exercises | Local, `reproduce.yml` | — |
| 22 | statsmodels 0.15.0 | all scripts, exercises | Local, `reproduce.yml` | — |
| 23 | Tableau | Hyper extract; every view's figure in SQL | Local, `reproduce.yml` | the clicks in Tableau Desktop |
| 24 | Power BI | every visual's figure in PostgreSQL | Local, `reproduce.yml` | the DAX itself, in Power BI |
| 25 | Data Studio (formerly Looker Studio) | CSV export; every chart's figure in PostgreSQL | Local, `reproduce.yml` | the clicks in Data Studio |
| 26 | Superset 6.1.0 | start-up, connection, dataset, SQL Lab, chart, exercises (through the API) | `ch26-superset.yml` | the same steps clicked in the web interface |
| 27 | Excel | report built with openpyxl, values checked | Local, `reproduce.yml` | opening the file in Excel |
| 28 | Streamlit 1.67.0 | app and AppTest tests | Local, `reproduce.yml` | — |
| 29 | FastAPI 0.163.1 | API and tests | Local, `reproduce.yml` | — |
| 30 | Flask 3.1.3 | app, exercises | Local, `reproduce.yml` | — |
| 31 | R Shiny 1.14.0 | server tests | `ch31-shiny.yml` | — |
| 32 | Great Expectations 1.25.0 | suites, checkpoint, quality gate | Local, `reproduce.yml` | — |
| 33 | Airflow 3.4.0 | install with constraints; `airflow dags test` of the nightly DAG | `ch33-airflow-install.yml`, `reproduce.yml`, Local | the clicks in the Airflow web interface |
| 34 | Prometheus 3.16.0 | exporter, scraping, alert rules, PromQL | `ch34-35-monitoring.yml` | — |
| 35 | Grafana 13.3.1 | provisioned data source and dashboard | `ch34-35-monitoring.yml` | — |

Steps marked "not executed" were written from the vendors' documentation of November 2026. Web
interfaces change several times a year; the chapters name each screen and field so that a moved
button can be found by its label.
