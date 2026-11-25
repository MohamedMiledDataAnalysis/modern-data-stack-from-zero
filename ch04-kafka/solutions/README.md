# Chapter 4 — corrections

> © 2026 Mohamed Miled. All rights reserved. This text is part of the book *The Modern Data Stack* and may not be copied, republished or sold. The code blocks are under the MIT licence (see `LICENSE`); the explanations are not (see `LICENSE-TEXT.md`).

- Exercise 1: `kafka-consumer-groups.sh ... --reset-offsets --to-earliest --execute`, then `python consumer.py`.
- Exercise 2: `python producer.py && python consumer.py`, then `SELECT COUNT(*) FROM orders_stream;`.
- Exercise 3: `exercise_3_one_partition.sql`.
- Exercise 4: `python producer.py`, then `kafka-consumer-groups.sh --describe --group meridian-loader`.
