#!/bin/bash
# Chapter 34 — start Prometheus v3.16.0 with this folder's configuration
docker run --name prometheus -d -p 9090:9090 \
  --add-host=host.docker.internal:host-gateway \
  -v "$PWD/prometheus.yml:/etc/prometheus/prometheus.yml" \
  -v "$PWD/alert_rules.yml:/etc/prometheus/alert_rules.yml" \
  prom/prometheus:v3.16.0
