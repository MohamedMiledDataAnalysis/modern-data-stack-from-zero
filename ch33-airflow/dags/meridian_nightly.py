"""Chapter 33 — Meridian's nightly pipeline, as an Airflow 3 DAG."""
from datetime import datetime
from pathlib import Path

import psycopg2
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task

REPO = Path.home() / 'meridian' / 'modern-data-stack-from-zero'
BOOK_VENV = Path.home() / 'meridian' / '.venv' / 'bin'   # the environment of Chapter 0


@dag(schedule='0 2 * * *', start_date=datetime(2026, 11, 1), catchup=False,
     tags=['meridian'], description='Check, transform, test and report every night')
def meridian_nightly():

    @task
    def count_orders():
        with psycopg2.connect(host='localhost', dbname='meridian_db',
                              user='meridian_user', password='meridian2024') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT COUNT(*) FROM fact_orders')
                n = cur.fetchone()[0]
        if n == 0:
            raise ValueError('fact_orders is empty: stopping the pipeline')
        print(f'{n:,} orders in the source')
        return n

    dbt_build = BashOperator(
        task_id='dbt_build',
        bash_command=f'cd {REPO}/ch14-dbt/meridian_dbt && '
                     f'{BOOK_VENV}/dbt build --profiles-dir ../profiles',
    )

    quality_gate = BashOperator(
        task_id='quality_gate',
        bash_command=f'cd {REPO}/ch32-great-expectations && '
                     f'{BOOK_VENV}/python quality_gate.py',
    )

    @task
    def report(n_orders: int):
        print(f'Nightly run complete: {n_orders:,} orders transformed and checked')

    n = count_orders()
    n >> dbt_build >> quality_gate >> report(n)


meridian_nightly()
