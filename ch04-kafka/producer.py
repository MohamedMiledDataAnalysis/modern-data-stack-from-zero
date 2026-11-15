"""Chapter 4 — publish the first 1,000 completed Meridian orders to Kafka."""
import json
from collections import Counter

from confluent_kafka import Producer
from sqlalchemy import create_engine, text

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)
producer = Producer({'bootstrap.servers': 'localhost:9092'})
per_partition = Counter()


def on_delivery(err, msg):
    """Called once per message, when the broker confirms (or refuses) it."""
    if err is not None:
        print('Delivery failed:', err)
    else:
        per_partition[msg.partition()] += 1


with engine.connect() as conn:
    rows = conn.execute(text(
        "SELECT order_id, customer_id, product_id, order_date, quantity, "
        "total_amount FROM fact_orders WHERE status = 'completed' "
        "ORDER BY order_id LIMIT 1000")).mappings().all()

for r in rows:
    event = {'order_id': r['order_id'], 'customer_id': r['customer_id'],
             'product_id': r['product_id'], 'order_date': r['order_date'].isoformat(),
             'quantity': r['quantity'], 'total_amount': float(r['total_amount'])}
    producer.produce('meridian.orders', key=str(r['customer_id']),
                     value=json.dumps(event), on_delivery=on_delivery)
    producer.poll(0)

producer.flush()
print(f'{sum(per_partition.values())} events published')
for p in sorted(per_partition):
    print(f'  partition {p}: {per_partition[p]}')
