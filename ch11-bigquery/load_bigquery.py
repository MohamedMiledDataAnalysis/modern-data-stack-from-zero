"""Creates the dataset and loads the five Meridian tables from PostgreSQL."""
import io

import pandas as pd
from google.cloud import bigquery
from sqlalchemy import create_engine

import os

from bq_config import DATASET, LOCATION, MODE, PG_URL, PROJECT, TABLES, bq_client

# Partition fact_orders only on a project with billing enabled: in the sandbox, partitions
# older than 60 days expire, and every order of 2021-2023 would be deleted at once.
PARTITION = os.environ.get('MERIDIAN_BQ_PARTITION') == '1'

SCHEMAS = {
    'dim_country': [('country_id', 'INT64'), ('country_name', 'STRING')],
    'dim_category': [('category_id', 'INT64'), ('category_name', 'STRING')],
    'dim_customer': [('customer_id', 'INT64'), ('first_name', 'STRING'), ('last_name', 'STRING'),
                     ('email', 'STRING'), ('country_id', 'INT64'), ('signup_date', 'DATE')],
    'dim_product': [('product_id', 'INT64'), ('product_name', 'STRING'),
                    ('category_id', 'INT64'), ('unit_price', 'NUMERIC')],
    'fact_orders': [('order_id', 'INT64'), ('customer_id', 'INT64'), ('product_id', 'INT64'),
                    ('order_date', 'DATE'), ('quantity', 'INT64'), ('unit_price', 'NUMERIC'),
                    ('total_amount', 'NUMERIC'), ('status', 'STRING')],
}

client = bq_client()
print('mode:', MODE)
dataset = bigquery.Dataset(f'{PROJECT}.{DATASET}')
dataset.location = LOCATION
client.create_dataset(dataset, exists_ok=True)

pg = create_engine(PG_URL)
for table in TABLES:
    df = pd.read_sql(f'SELECT * FROM {table}', pg)
    if table == 'fact_orders' and MODE == 'local':
        # the emulator stalls on 250,000 rows: test on the first quarter of 2023
        df = df[(df.order_date >= pd.Timestamp('2023-01-01').date())
                & (df.order_date <= pd.Timestamp('2023-03-31').date())]
    schema = [bigquery.SchemaField(name, kind) for name, kind in SCHEMAS[table]]
    if table == 'fact_orders' and MODE == 'gcp' and PARTITION:
        # partitioned by order date, clustered by status: queries on a month read only that month
        bq_table = bigquery.Table(f'{PROJECT}.{DATASET}.{table}', schema=schema)
        bq_table.time_partitioning = bigquery.TimePartitioning(field='order_date')
        bq_table.clustering_fields = ['status']
        client.delete_table(bq_table, not_found_ok=True)
        client.create_table(bq_table)
    buf = io.BytesIO(df.to_csv(index=False).encode())
    config = bigquery.LoadJobConfig(schema=schema, source_format=bigquery.SourceFormat.CSV,
                                    skip_leading_rows=1,
                                    write_disposition='WRITE_TRUNCATE')
    job = client.load_table_from_file(buf, f'{PROJECT}.{DATASET}.{table}', job_config=config)
    job.result()                                  # waits for the load job to finish
    rows = client.get_table(f'{PROJECT}.{DATASET}.{table}').num_rows
    print(f'{table:<13}{rows:>8,} rows')
    if MODE == 'gcp' and table == 'fact_orders' and PARTITION:
        print('partitioned by', client.get_table(f'{PROJECT}.{DATASET}.{table}').time_partitioning.field)
