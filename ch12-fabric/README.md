# Chapter 12 — Microsoft Fabric

- `python export_parquet.py` — writes the five tables to `upload/` with exact types, for upload to the lakehouse
- `notebook/meridian_lakehouse.py` — the notebook cells; also runs locally with Spark on `upload/`
- `tsql/queries.sql` — for the SQL analytics endpoint
- `tsql/create_warehouse_tables.sql` — for the warehouse (Fabric only)
- `solutions/exercises.sql` — corrections

Practise the T-SQL locally on SQL Server 2022, in the container of Chapter 2, Step 8 (`pymssql` is in `requirements.txt`). From this folder, after `python export_parquet.py`:

```bash
docker start sqlserver   # the container of Chapter 2, Step 8
# or, if you skipped that step: bash ../ch02-files-apis-iot/sqlserver/start_sqlserver.sh
docker logs sqlserver 2>&1 | grep "Recovery is complete"   # repeat until it prints a line
python tsql/load_sqlserver.py
python tsql/run_sql.py tsql/queries.sql
python tsql/run_sql.py solutions/exercises.sql
```
