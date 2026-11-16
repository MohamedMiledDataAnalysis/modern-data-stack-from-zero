"""Chapter 26 corrections, through the REST API. Run superset_api.py first.
    python solutions/exercises.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from client import BASE, find, session                # noqa: E402

s = session()
db_id = find(s, 'database', 'database_name', 'Meridian')

print('Exercise 1 - a virtual dataset: orders with their country')
SQL = """SELECT o.order_id, o.order_date, o.status, o.total_amount, c.country_name
FROM fact_orders o
JOIN dim_customer cu ON cu.customer_id = o.customer_id
JOIN dim_country c ON c.country_id = cu.country_id"""
vds_id = find(s, 'dataset', 'table_name', 'orders_with_country')
if vds_id is None:
    r = s.post(f'{BASE}/api/v1/dataset/', json={
        'database': db_id, 'schema': 'public', 'table_name': 'orders_with_country', 'sql': SQL})
    r.raise_for_status()
    vds_id = r.json()['id']

print('Exercise 2 - a saved metric, used for 2023 revenue per country')
ds = s.get(f'{BASE}/api/v1/dataset/{vds_id}').json()['result']
if not any(m['metric_name'] == 'revenue' for m in ds['metrics']):
    metrics = [{'id': m['id'], 'metric_name': m['metric_name'], 'expression': m['expression']}
               for m in ds['metrics']]
    metrics.append({'metric_name': 'revenue', 'expression': 'SUM(total_amount)',
                    'verbose_name': 'Revenue', 'd3format': ',.2f'})
    s.put(f'{BASE}/api/v1/dataset/{vds_id}', json={'metrics': metrics}).raise_for_status()
query_context = {
    'datasource': {'id': vds_id, 'type': 'table'},
    'queries': [{
        'columns': ['country_name'], 'metrics': ['revenue'],
        'filters': [{'col': 'status', 'op': '==', 'val': 'completed'},
                    {'col': 'order_date', 'op': 'TEMPORAL_RANGE',
                     'val': '2023-01-01 : 2024-01-01'}],
        'orderby': [['revenue', False]], 'row_limit': 10,
    }],
    'result_format': 'json', 'result_type': 'full',
}
r = s.post(f'{BASE}/api/v1/chart/data', json=query_context)
r.raise_for_status()
for row in r.json()['result'][0]['data']:
    print(f"{row['country_name']:<12}{row['revenue']:>14,.2f}")

print('Exercise 3 - a dashboard holding the chart of Step 5')
chart_id = find(s, 'chart', 'slice_name', 'Completed revenue per year')
dash_id = find(s, 'dashboard', 'dashboard_title', 'Meridian overview')
if dash_id is None:
    r = s.post(f'{BASE}/api/v1/dashboard/', json={'dashboard_title': 'Meridian overview',
                                                  'published': True})
    r.raise_for_status()
    dash_id = r.json()['id']
s.put(f'{BASE}/api/v1/chart/{chart_id}', json={'dashboards': [dash_id]}).raise_for_status()
charts = s.get(f'{BASE}/api/v1/dashboard/{dash_id}/charts').json()['result']
print('dashboard', dash_id, 'charts:', [c['slice_name'] for c in charts])
print('url:', s.get(f'{BASE}/api/v1/dashboard/{dash_id}').json()['result']['url'])
