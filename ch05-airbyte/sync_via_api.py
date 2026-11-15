"""Chapter 5 — create the Meridian source, destination and connection with
Airbyte's API, run one sync, and print the result.

Usage: python sync_via_api.py <client_id> <client_secret> <db_host>
(client id and secret come from:  abctl local credentials)
"""
import sys
import time

import requests

BASE = 'http://localhost:8000/api/public/v1'
client_id, client_secret, db_host = sys.argv[1:4]

token = requests.post('http://localhost:8000/api/v1/applications/token', json={
    'client_id': client_id, 'client_secret': client_secret,
    'grant-type': 'client_credentials'}, timeout=30).json()['access_token']
H = {'Authorization': f'Bearer {token}'}


def call(method, path, **kw):
    r = requests.request(method, BASE + path, headers=H, timeout=120, **kw)
    if r.status_code >= 400:
        print(method, path, r.status_code, r.text[:3000])
        r.raise_for_status()
    return r.json()


ws = call('GET', '/workspaces')['data'][0]['workspaceId']
print('workspace', ws)
pg = {'host': db_host, 'port': 5432, 'database': 'meridian_db',
      'username': 'meridian_user', 'password': 'meridian2024',
      'tunnel_method': {'tunnel_method': 'NO_TUNNEL'}}
src = call('POST', '/sources', json={
    'name': 'Meridian PostgreSQL', 'workspaceId': ws,
    'configuration': {'sourceType': 'postgres', **pg, 'schemas': ['public'],
                      'ssl_mode': {'mode': 'disable'},
                      'replication_method': {'method': 'Standard'}}})
print('source', src['sourceId'])
dst = call('POST', '/destinations', json={
    'name': 'Meridian raw (PostgreSQL)', 'workspaceId': ws,
    'configuration': {'destinationType': 'postgres', **pg, 'schema': 'airbyte_raw',
                      'ssl_mode': {'mode': 'disable'}}})
print('destination', dst['destinationId'])
con = call('POST', '/connections', json={
    'name': 'Meridian to raw', 'sourceId': src['sourceId'],
    'destinationId': dst['destinationId'],
    'configurations': {'streams': [
        {'name': 'dim_product', 'syncMode': 'full_refresh_overwrite'},
        {'name': 'fact_orders', 'syncMode': 'incremental_append',
         'cursorField': ['order_id']}]},
    'schedule': {'scheduleType': 'manual'}})
print('connection', con['connectionId'])
job = call('POST', '/jobs', json={'connectionId': con['connectionId'], 'jobType': 'sync'})
jid = job['jobId']
while True:
    j = call('GET', f'/jobs/{jid}')
    if j['status'] not in ('pending', 'running'):
        break
    time.sleep(10)
print('job', jid, j['status'], 'rows', j.get('rowsSynced'), 'bytes', j.get('bytesSynced'),
      'duration', j.get('duration'))
