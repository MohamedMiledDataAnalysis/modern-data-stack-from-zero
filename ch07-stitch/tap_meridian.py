"""A minimal Singer tap: reads Meridian orders and writes Singer messages to stdout.

Usage:  python tap_meridian.py [--state state.json] | python target_jsonl.py
"""
import argparse
import json
import sys

import psycopg2

STREAM = 'fact_orders'
SCHEMA = {
    'type': 'object',
    'properties': {
        'order_id': {'type': 'integer'},
        'customer_id': {'type': 'integer'},
        'product_id': {'type': 'integer'},
        'order_date': {'type': 'string', 'format': 'date'},
        'quantity': {'type': 'integer'},
        'total_amount': {'type': 'number'},
        'status': {'type': 'string'},
    },
}


def emit(message):
    sys.stdout.write(json.dumps(message) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', help='file holding the last STATE message value')
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args()

    bookmark = 0
    if args.state:
        with open(args.state) as f:
            bookmark = json.load(f).get('bookmarks', {}).get(STREAM, {}).get('order_id', 0)

    emit({'type': 'SCHEMA', 'stream': STREAM, 'schema': SCHEMA,
          'key_properties': ['order_id'], 'bookmark_properties': ['order_id']})

    conn = psycopg2.connect(host='localhost', dbname='meridian_db',
                            user='meridian_user', password='meridian2024')
    cur = conn.cursor()
    sql = ('SELECT order_id, customer_id, product_id, order_date, quantity, '
           'total_amount, status FROM fact_orders WHERE order_id > %s ORDER BY order_id')
    if args.limit:
        sql += f' LIMIT {int(args.limit)}'
    cur.execute(sql, (bookmark,))

    last = bookmark
    for n, row in enumerate(cur, start=1):
        record = dict(zip(SCHEMA['properties'], row))
        record['order_date'] = record['order_date'].isoformat()
        record['total_amount'] = float(record['total_amount'])
        emit({'type': 'RECORD', 'stream': STREAM, 'record': record})
        last = record['order_id']
        if n % 1000 == 0:                       # a checkpoint every 1,000 rows
            emit({'type': 'STATE', 'value': {'bookmarks': {STREAM: {'order_id': last}}}})
    emit({'type': 'STATE', 'value': {'bookmarks': {STREAM: {'order_id': last}}}})
    conn.close()


if __name__ == '__main__':
    main()
