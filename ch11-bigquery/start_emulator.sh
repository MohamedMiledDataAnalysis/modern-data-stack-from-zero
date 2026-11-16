#!/bin/bash
# The BigQuery emulator, with an empty project meridian-local
docker run --name bq-emulator -d -p 9050:9050 \
  ghcr.io/goccy/bigquery-emulator:0.8.1 --project=meridian-local
