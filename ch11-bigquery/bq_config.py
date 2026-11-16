"""Where the Chapter 11 scripts connect.

MERIDIAN_BQ_MODE=local (default): the BigQuery emulator on localhost:9050 (start_emulator.sh).
MERIDIAN_BQ_MODE=gcp: Google BigQuery, project MERIDIAN_GCP_PROJECT, after
                      gcloud auth application-default login.
"""
import os

from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from google.cloud import bigquery

MODE = os.environ.get('MERIDIAN_BQ_MODE', 'local')
PROJECT = os.environ.get('MERIDIAN_GCP_PROJECT', 'meridian-local')
DATASET = 'meridian'
LOCATION = 'europe-west2'                     # London
PG_URL = 'postgresql+psycopg2://meridian_user:meridian2024@localhost:5432/meridian_db'
TABLES = ['dim_country', 'dim_category', 'dim_customer', 'dim_product', 'fact_orders']


def bq_client():
    if MODE == 'gcp':
        return bigquery.Client(project=PROJECT, location=LOCATION)
    return bigquery.Client(project=PROJECT, credentials=AnonymousCredentials(),
                           client_options=ClientOptions(api_endpoint='http://localhost:9050'))
