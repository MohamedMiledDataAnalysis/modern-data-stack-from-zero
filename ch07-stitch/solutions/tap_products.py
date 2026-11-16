"""Exercise 3 - a full-table stream for dim_product: no bookmark, every run copies every row."""
import json
import sys

import psycopg2

STREAM = 'dim_product'
SCHEMA = {'type': 'object', 'properties': {
    'product_id': {'type': 'integer'},
    'product_name': {'type': 'string'},
    'category_id': {'type': 'integer'},
    'unit_price': {'type': 'number'},
}}


def emit(message):
    sys.stdout.write(json.dumps(message) + '\n')


emit({'type': 'SCHEMA', 'stream': STREAM, 'schema': SCHEMA, 'key_properties': ['product_id']})
with psycopg2.connect(host='localhost', dbname='meridian_db',
                      user='meridian_user', password='meridian2024') as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT product_id, product_name, category_id, unit_price '
                    'FROM dim_product ORDER BY product_id')
        for row in cur:
            record = dict(zip(SCHEMA['properties'], row))
            record['unit_price'] = float(record['unit_price'])
            emit({'type': 'RECORD', 'stream': STREAM, 'record': record})
emit({'type': 'STATE', 'value': {}})
