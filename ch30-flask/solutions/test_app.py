"""Exercise 2 — test the Flask routes.

Run from the ch30-flask folder:  python -m pytest solutions/test_app.py -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import app   # noqa: E402

client = app.test_client()


def test_2021_has_12_months():
    page = client.get('/?year=2021').get_data(as_text=True)
    assert page.count('<tr><td>') == 12


def test_order_1_is_found():
    page = client.post('/order', data={'order_id': '1'}).get_data(as_text=True)
    assert 'Order 1: 2 item(s) on 2023-01-30' in page


def test_unknown_year():
    assert client.get('/api/revenue/1999').status_code == 404
