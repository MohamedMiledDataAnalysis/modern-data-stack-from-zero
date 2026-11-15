# Chapter 4 — Apache Kafka

- `start_kafka.sh` — starts Kafka 4.4.0 in Docker and creates `meridian.orders` (3 partitions).
- `producer.py` — publishes 1,000 completed orders, keyed by customer.
- `consumer.py [name]` — group `meridian-loader`; writes events to `orders_stream` in PostgreSQL.
- `solutions/` — corrections to the exercises.

Install the client once: `pip install confluent-kafka==2.16.1` (already in the book's `requirements.txt`).
