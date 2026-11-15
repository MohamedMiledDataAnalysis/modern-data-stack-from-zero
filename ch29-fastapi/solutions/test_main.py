"""Exercise 3 — test the API without starting a server.

Run from the ch29-fastapi folder:  python -m pytest solutions/test_main.py -q
"""
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from main import app   # noqa: E402

client = TestClient(app)
ALEX = {'sessions_90d': 2, 'support_tickets_90d': 3, 'days_since_login': 95,
        'newsletter_opt_in': False, 'uses_app': False}


def test_order_1():
    r = client.get('/orders/1')
    assert r.status_code == 200
    assert r.json()['total_amount'] == 933.32


def test_unknown_order():
    assert client.get('/orders/999999').status_code == 404


def test_revenue_september_2023():
    assert client.get('/revenue', params={'month': '2023-09'}).json()['orders'] == 4161


def test_bad_month_is_rejected():
    assert client.get('/revenue', params={'month': 'Sept'}).status_code == 422


def test_alex():
    body = client.post('/churn', json=ALEX).json()
    assert body == {'churn_probability': 0.9222, 'at_risk': True}
