#!/bin/bash
# Chapter 3 — create the folders and start Apache NiFi 2.12.0 in Docker
mkdir -p ~/meridian/nifi/drops ~/meridian/nifi/landed ~/meridian/nifi/quarantine
docker run --name nifi -d -p 8443:8443 \
  -e SINGLE_USER_CREDENTIALS_USERNAME=admin \
  -e SINGLE_USER_CREDENTIALS_PASSWORD=meridian-nifi-2026 \
  -v ~/meridian/nifi:/data \
  apache/nifi:2.12.0
echo "NiFi is starting. Follow it with: docker logs -f nifi"
echo "Then open https://localhost:8443/nifi (user admin)"
