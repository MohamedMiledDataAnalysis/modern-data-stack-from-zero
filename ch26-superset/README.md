# Chapter 26 — Apache Superset

```bash
bash start_superset.sh          # builds the image (Superset 6.1.0 + psycopg2), starts it on :8088
python superset_api.py          # connection, dataset, SQL Lab query and chart through the REST API
python solutions/exercises.py   # virtual dataset, saved metric, dashboard
```

Sign in at http://localhost:8088 as admin / meridian2026.

On WSL, Superset reaches PostgreSQL at Ubuntu's own address, not `host.docker.internal`:
`export MERIDIAN_PG_HOST=$(hostname -I | awk '{print $1}')` before `python superset_api.py`.
