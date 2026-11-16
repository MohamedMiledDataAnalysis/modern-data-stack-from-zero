#!/bin/bash
# Chapter 35 — start Grafana 13.3.1 with Meridian's data source and dashboard
docker run --name grafana -d -p 3000:3000 \
  --add-host=host.docker.internal:host-gateway \
  -e GF_SECURITY_ADMIN_PASSWORD=meridian2026 \
  -v "$PWD/provisioning:/etc/grafana/provisioning" \
  -v "$PWD/dashboards:/var/lib/grafana/dashboards" \
  grafana/grafana:13.3.1
