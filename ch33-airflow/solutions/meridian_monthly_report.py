"""Chapter 33, Exercise 2 — a monthly report DAG: on the 1st, report the previous month."""
from datetime import datetime
from pathlib import Path

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag

REPO = Path.home() / 'meridian' / 'modern-data-stack-from-zero'
BOOK_VENV = Path.home() / 'meridian' / '.venv' / 'bin'


@dag(schedule='30 6 1 * *', start_date=datetime(2023, 1, 1), catchup=False,
     tags=['meridian'], description='Monthly report for the previous month')
def meridian_monthly_report():
    BashOperator(
        task_id='papermill_report',
        bash_command=(
            f'cd {REPO}/ch20-jupyter && mkdir -p reports && '
            f'{BOOK_VENV}/papermill monthly_report.ipynb '
            'reports/report_{{ macros.ds_format(macros.ds_add(ds, -1), "%Y-%m-%d", "%Y-%m") }}.ipynb '
            '-p month {{ macros.ds_format(macros.ds_add(ds, -1), "%Y-%m-%d", "%Y-%m") }}'
        ),
    )


meridian_monthly_report()
