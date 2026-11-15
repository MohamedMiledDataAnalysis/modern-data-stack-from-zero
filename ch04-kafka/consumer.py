"""Chapter 4 — read order events and write them to PostgreSQL."""
import json
import sys
from collections import Counter

from confluent_kafka import Consumer
from sqlalchemy import create_engine, text

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)
name = sys.argv[1] if len(sys.argv) > 1 else 'loader-1'

consumer = Consumer({'bootstrap.servers': 'localhost:9092',
                     'group.id': 'meridian-loader',
                     'client.id': name,
                     'auto.offset.reset': 'earliest',
                     'enable.auto.commit': False})
consumer.subscribe(['meridian.orders'])

with engine.begin() as conn:
    conn.execute(text(
        'CREATE TABLE IF NOT EXISTS orders_stream ('
        ' order_id INTEGER PRIMARY KEY, customer_id INTEGER,'
        ' total_amount NUMERIC(10,2), kafka_partition INTEGER,'
        ' kafka_offset BIGINT)'))

seen = Counter()
idle = 0
while idle < 10:                       # stop after 10 empty polls of 1 second
    msg = consumer.poll(1.0)
    if msg is None:
        idle += 1
        continue
    if msg.error():
        print('Error:', msg.error())
        continue
    idle = 0
    e = json.loads(msg.value())
    with engine.begin() as conn:
        conn.execute(text(
            'INSERT INTO orders_stream VALUES (:o, :c, :t, :p, :off) '
            'ON CONFLICT (order_id) DO NOTHING'),
            {'o': e['order_id'], 'c': e['customer_id'], 't': e['total_amount'],
             'p': msg.partition(), 'off': msg.offset()})
    consumer.commit(message=msg, asynchronous=False)
    seen[msg.partition()] += 1

consumer.close()
print(f'{name}: {sum(seen.values())} events read', dict(sorted(seen.items())))
