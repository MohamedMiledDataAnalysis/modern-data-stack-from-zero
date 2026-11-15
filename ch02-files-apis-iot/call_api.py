"""Chapter 2, Step 4 — call the product API."""
import os

import requests

BASE = 'http://localhost:8100/v1'
HEADERS = {'X-API-Key': os.environ.get('MERIDIAN_API_KEY', 'meridian-demo-key')}

resp = requests.get(f'{BASE}/products/1', headers=HEADERS, timeout=10)
print(resp.status_code)
print(resp.json())

# Read every page until the API says there is no next page
products, page = [], 1
while page is not None:
    resp = requests.get(f'{BASE}/products', headers=HEADERS,
                        params={'page': page, 'page_size': 100}, timeout=10)
    resp.raise_for_status()
    body = resp.json()
    products.extend(body['items'])
    print(f"page {body['page']}: {len(body['items'])} products")
    page = body['next_page']
print(f'{len(products)} products downloaded')
