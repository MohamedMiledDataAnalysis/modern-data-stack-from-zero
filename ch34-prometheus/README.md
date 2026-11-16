# Chapter 34 — Prometheus

From this folder:

1. `python meridian_exporter.py` — metrics at http://localhost:8001/metrics
2. `bash start_prometheus.sh` — Prometheus v3.16.0 at http://localhost:9090

`alert_rules.yml` holds the four alerts. Check the files with:
`docker run --rm -v "$PWD:/cfg" --entrypoint promtool prom/prometheus:v3.16.0 check config /cfg/prometheus.yml`
