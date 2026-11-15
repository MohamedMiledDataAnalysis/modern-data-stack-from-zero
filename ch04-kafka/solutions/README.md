# Chapter 4 — corrections

- Exercise 1: `kafka-consumer-groups.sh ... --reset-offsets --to-earliest --execute`, then `python consumer.py`.
- Exercise 2: `python producer.py && python consumer.py`, then `SELECT COUNT(*) FROM orders_stream;`.
- Exercise 3: `exercise_3_one_partition.sql`.
- Exercise 4: `python producer.py`, then `kafka-consumer-groups.sh --describe --group meridian-loader`.
