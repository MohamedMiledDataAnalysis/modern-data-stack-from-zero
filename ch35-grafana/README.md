# Chapter 35 — Grafana

With Prometheus and the exporter of Chapter 34 running, from this folder:

`bash start_grafana.sh` — Grafana 13.3.1 at http://localhost:3000 (user `admin`, password `meridian2026`)

- `provisioning/datasources/prometheus.yml` — the Prometheus data source
- `provisioning/dashboards/meridian.yml` — where Grafana finds dashboards
- `dashboards/meridian.json` — the *Meridian platform health* dashboard
