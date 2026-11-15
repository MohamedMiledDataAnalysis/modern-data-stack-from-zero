#!/bin/bash
# Chapter 4 — start a single Kafka 4.4.0 broker (KRaft mode) and create the topic
docker run --name kafka -d -p 9092:9092 apache/kafka:4.4.0
echo "Waiting for the broker..."
until docker exec kafka /opt/kafka/bin/kafka-topics.sh \
        --bootstrap-server localhost:9092 --list >/dev/null 2>&1; do sleep 2; done
docker exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic meridian.orders --partitions 3 --replication-factor 1
docker exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --topic meridian.orders
