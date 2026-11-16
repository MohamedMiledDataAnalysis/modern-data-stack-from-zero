#!/bin/bash
# Chapter 2, Step 8 - start SQL Server 2022 in Docker (the same container Chapter 12 uses).
# On a Mac with Apple Silicon, first tick "Use Rosetta for x86_64/amd64 emulation" in Docker Desktop.
docker run --name sqlserver -e ACCEPT_EULA=Y -e 'MSSQL_SA_PASSWORD=Meridian2026!' \
  -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
echo "SQL Server is starting: wait about 20 seconds before the next command."
