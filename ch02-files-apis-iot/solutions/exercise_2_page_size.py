"""Exercise 2 — download all products 50 at a time and count the requests."""
import requests

BASE = 'http://localhost:8100/v1'
HEADERS = {'X-API-Key': 'meridian-demo-key'}
products, page, calls = [], 1, 0
while page is not None:
    body = requests.get(f'{BASE}/products', headers=HEADERS,
                        params={'page': page, 'page_size': 50}, timeout=10).json()
    calls += 1
    products.extend(body['items'])
    page = body['next_page']
print(f'{len(products)} products in {calls} requests')
