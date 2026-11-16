# Chapter 12 — Microsoft Fabric

- `python export_parquet.py` — writes the five tables to `upload/` with exact types, for upload to the lakehouse
- `notebook/meridian_lakehouse.py` — the notebook cells; also runs locally with Spark on `upload/`
- `tsql/queries.sql` — for the SQL analytics endpoint
- `tsql/create_warehouse_tables.sql` — for the warehouse (Fabric only)
- `solutions/exercises.sql` — corrections

Practise the T-SQL locally on SQL Server 2022:

```bash
docker run -e ACCEPT_EULA=Y -e MSSQL_SA_PASSWORD='Meridian2026!' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
pip install pymssql==2.4.6
python tsql/load_sqlserver.py
python tsql/run_sql.py tsql/queries.sql
```
