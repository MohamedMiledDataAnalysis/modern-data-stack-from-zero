#!/bin/bash
# Chapter 9 — start fake-gcs-server, a Cloud Storage emulator, on port 4443
docker run --name fake-gcs -d -p 4443:4443 \
  fsouza/fake-gcs-server:1.52 -scheme http -port 4443 -external-url http://localhost:4443
