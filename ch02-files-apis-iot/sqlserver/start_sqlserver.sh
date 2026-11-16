#!/bin/bash
# Chapter 2, Step 8 - start SQL Server 2022 in Docker (the same container Chapter 12 uses).
# On a Mac with Apple silicon, first tick "Use Rosetta for x86_64/amd64 emulation on Apple Silicon"
# in Docker Desktop -> Settings -> General. --platform linux/amd64 fetches the x86-64 image
# without a platform warning; it changes nothing on an x86-64 machine.
docker run --name sqlserver --platform linux/amd64 \
  -e ACCEPT_EULA=Y -e 'MSSQL_SA_PASSWORD=Meridian2026!' \
  -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
echo "SQL Server is starting. Check that it is ready with:"
echo '  docker logs sqlserver 2>&1 | grep "Recovery is complete"'
