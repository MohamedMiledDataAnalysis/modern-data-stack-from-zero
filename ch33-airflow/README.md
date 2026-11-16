# Chapter 33 — Apache Airflow

Airflow has its own environment (see the chapter):

```bash
python3.13 -m venv ~/meridian/airflow-venv && source ~/meridian/airflow-venv/bin/activate
pip install "apache-airflow==3.4.0" psycopg2-binary==2.9.13 \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.4.0/constraints-3.13.txt"
export AIRFLOW_HOME=~/meridian/airflow
export AIRFLOW__CORE__DAGS_FOLDER=~/meridian/modern-data-stack-from-zero/ch33-airflow/dags
export AIRFLOW__CORE__LOAD_EXAMPLES=False
airflow dags test meridian_nightly
```

- `dags/meridian_nightly.py` — count, dbt build, quality gate, report
- `solutions/meridian_monthly_report.py` — Exercise 2 (copy it into `dags/`)
