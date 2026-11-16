"""Signs in to the Superset REST API and returns a ready session."""
import json
import os

import requests

BASE = os.environ.get('SUPERSET_URL', 'http://localhost:8088')


def session():
    s = requests.Session()
    token = s.post(f'{BASE}/api/v1/security/login', json={
        'username': 'admin', 'password': 'meridian2026', 'provider': 'db', 'refresh': True,
    }).json()['access_token']
    s.headers['Authorization'] = f'Bearer {token}'
    s.headers['X-CSRFToken'] = s.get(f'{BASE}/api/v1/security/csrf_token/').json()['result']
    s.headers['Referer'] = BASE
    return s


def find(s, kind, column, value):
    """The id of the first object of this kind whose column equals value, or None."""
    q = json.dumps({'filters': [{'col': column, 'opr': 'eq', 'value': value}]})
    result = s.get(f'{BASE}/api/v1/{kind}/', params={'q': q}).json()['result']
    return result[0]['id'] if result else None
