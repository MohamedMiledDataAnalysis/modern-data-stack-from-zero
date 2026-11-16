"""Drives Superset through its REST API: the same steps as the clicks of Chapter 26.

Connects Superset to the Meridian database, registers fact_orders as a dataset,
runs a query in SQL Lab, and builds a chart whose data it then reads back.
"""
import json
import os

from client import BASE, find, session

PG_HOST = os.environ.get('MERIDIAN_PG_HOST', 'host.docker.internal')
s = session()

# 1. The database connection
uri = f'postgresql://meridian_user:meridian2024@{PG_HOST}:5432/meridian_db'
db_id = find(s, 'database', 'database_name', 'Meridian')
if db_id is None:
    r = s.post(f'{BASE}/api/v1/database/', json={
        'database_name': 'Meridian', 'sqlalchemy_uri': uri, 'expose_in_sqllab': True})
    r.raise_for_status()
    db_id = r.json()['id']
print('database id:', db_id)

# 2. The dataset
ds_id = find(s, 'dataset', 'table_name', 'fact_orders')
if ds_id is None:
    r = s.post(f'{BASE}/api/v1/dataset/', json={
        'database': db_id, 'schema': 'public', 'table_name': 'fact_orders'})
    r.raise_for_status()
    ds_id = r.json()['id']
columns = s.get(f'{BASE}/api/v1/dataset/{ds_id}').json()['result']['columns']
print('dataset id:', ds_id, 'columns:', ', '.join(c['column_name'] for c in columns))

# 3. SQL Lab
r = s.post(f'{BASE}/api/v1/sqllab/execute/', json={
    'database_id': db_id, 'schema': 'public', 'runAsync': False,
    'sql': "SELECT status, COUNT(*) AS orders FROM fact_orders GROUP BY status ORDER BY orders DESC"})
r.raise_for_status()
for row in r.json()['data']:
    print('SQL Lab:', row)

# 4. A chart: completed revenue per year, as a bar chart
params = {
    'datasource': f'{ds_id}__table', 'viz_type': 'echarts_timeseries_bar',
    'x_axis': 'order_date', 'time_grain_sqla': 'P1Y',
    'metrics': [{'expressionType': 'SQL', 'sqlExpression': 'SUM(total_amount)',
                 'label': 'Revenue'}],
    'adhoc_filters': [{'expressionType': 'SIMPLE', 'clause': 'WHERE', 'subject': 'status',
                       'operator': '==', 'comparator': 'completed'}],
    'row_limit': 1000,
}
query_context = {
    'datasource': {'id': ds_id, 'type': 'table'},
    'queries': [{
        'columns': [{'columnType': 'BASE_AXIS', 'sqlExpression': 'order_date',
                     'label': 'order_date', 'expressionType': 'SQL', 'timeGrain': 'P1Y'}],
        'metrics': params['metrics'],
        'filters': [{'col': 'status', 'op': '==', 'val': 'completed'}],
        'orderby': [[{'expressionType': 'SQL', 'sqlExpression': 'order_date'}, True]],
        'row_limit': 1000,
    }],
    'form_data': params, 'result_format': 'json', 'result_type': 'full',
}
chart_id = find(s, 'chart', 'slice_name', 'Completed revenue per year')
if chart_id is None:
    r = s.post(f'{BASE}/api/v1/chart/', json={
        'slice_name': 'Completed revenue per year', 'viz_type': 'echarts_timeseries_bar',
        'datasource_id': ds_id, 'datasource_type': 'table', 'params': json.dumps(params),
        'query_context': json.dumps(query_context)})
    r.raise_for_status()
    chart_id = r.json()['id']
print('chart id:', chart_id)

r = s.get(f'{BASE}/api/v1/chart/{chart_id}/data/')
if r.status_code != 200:                      # older charts have no saved query context
    print('saved-context read:', r.status_code, r.text[:200])
    r = s.post(f'{BASE}/api/v1/chart/data', json=query_context)
r.raise_for_status()
for row in r.json()['result'][0]['data']:
    print('chart data:', row)
