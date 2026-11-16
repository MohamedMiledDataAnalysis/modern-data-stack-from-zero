#!/bin/bash
# Builds the image, starts Superset on http://localhost:8088 and creates the admin user.
set -e
cd "$(dirname "$0")"
docker build -q -t meridian-superset .
docker run -d --name superset -p 8088:8088 \
  -e SUPERSET_SECRET_KEY="$(openssl rand -base64 42)" \
  --add-host=host.docker.internal:host-gateway \
  meridian-superset
sleep 10
docker exec superset superset db upgrade > /dev/null 2>&1
docker exec superset superset fab create-admin --username admin --password meridian2026 \
  --firstname Amina --lastname Admin --email admin@meridian.example
docker exec superset superset init > /dev/null 2>&1
echo "Superset is ready: http://localhost:8088  (admin / meridian2026)"
