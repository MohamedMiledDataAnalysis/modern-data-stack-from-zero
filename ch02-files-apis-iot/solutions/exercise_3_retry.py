"""Exercise 3 — retry a request three times, waiting longer each time."""
import time

import requests


def get_with_retry(url, headers, attempts=3, wait=1.0):
    for attempt in range(1, attempts + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code < 500:
                return resp
            print(f'attempt {attempt}: '
                  f'server error {resp.status_code}')
        except requests.ConnectionError:
            print(f'attempt {attempt}: cannot connect')
        if attempt < attempts:
            time.sleep(wait)
            wait *= 2
    raise RuntimeError(
        f'{url} failed after {attempts} attempts')


if __name__ == '__main__':
    r = get_with_retry('http://localhost:8100/v1/products/1',
                       {'X-API-Key': 'meridian-demo-key'})
    print(r.status_code, r.json()['product_name'])
