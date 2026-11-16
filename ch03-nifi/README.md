# Chapter 3 — Apache NiFi

- `start_nifi.sh` — creates `~/meridian/nifi/{drops,landed,quarantine}` and starts NiFi 2.12.0.
- `supplier_stock.avsc` — the schema to paste into the CSVReader's *Schema Text*.

## Processor settings used in the chapter

| Processor / service | Property | Value |
|:--|:--|:--|
| GetFile | Input Directory | `/data/drops` |
| GetFile | File Filter | `.*\.csv` |
| GetFile | Keep Source File | `false` |
| CSVReader | Schema Access Strategy | `Use 'Schema Text' Property` |
| CSVReader | Schema Text | content of `supplier_stock.avsc` |
| CSVReader | Treat First Line as Header | `true` |
| CSVReader | Date Format | `yyyy-MM-dd` |
| ValidateRecord | Record Reader / Writer | `CSVReader` / `JsonRecordSetWriter` |
| ValidateRecord | Allow Extra Fields | `false` |
| PutFile "Write landed" | Directory | `/data/landed` |
| PutFile "Write quarantine" | Directory | `/data/quarantine` |

## Connections

| From | Relationship | To |
|:--|:--|:--|
| GetFile | success | ValidateRecord |
| ValidateRecord | valid | Write landed |
| ValidateRecord | invalid, failure | Write quarantine |
| both PutFile | success | terminate |
| both PutFile | failure | the same PutFile (a loop back onto itself) |

## Exercise 4 (QueryRecord)

| Processor / service | Property | Value |
|:--|:--|:--|
| QueryRecord | Record Reader / Writer | `JsonTreeReader` / `JsonRecordSetWriter` |
| QueryRecord | accepted | `SELECT * FROM FLOWFILE WHERE stock_qty >= 0` → Write landed |
| QueryRecord | negative | `SELECT * FROM FLOWFILE WHERE stock_qty < 0` → Write quarantine |
| QueryRecord | failure / original | Write quarantine / terminate |

## Writing to PostgreSQL instead of a folder (not run by the test workflow)

`<host>` is `host.docker.internal` on macOS, and the first value of `hostname -I` on Ubuntu and WSL.

Write to a new table, so that Chapter 2's `supplier_stock` keeps its 500 rows. Create it first, as `meridian_user`:

```sql
CREATE TABLE supplier_stock_nifi (product_id INTEGER, supplier TEXT,
  stock_qty INTEGER, reorder_level INTEGER, updated DATE);
```

| Processor / service | Property | Value |
|:--|:--|:--|
| DBCPConnectionPool | Database Connection URL | `jdbc:postgresql://<host>:5432/meridian_db` |
| DBCPConnectionPool | Database Driver Class Name | `org.postgresql.Driver` |
| DBCPConnectionPool | Database Driver Location(s) | `/data/postgresql-<version>.jar` (the file you downloaded) |
| DBCPConnectionPool | Database User / Password | `meridian_user` / `meridian2024` |
| JsonTreeReader | Schema Access Strategy / Schema Text | `Use 'Schema Text' Property` / content of `supplier_stock.avsc` |
| PutDatabaseRecord | Record Reader | `JsonTreeReader` |
| PutDatabaseRecord | Database Type / Statement Type | `PostgreSQL` / `INSERT` |
| PutDatabaseRecord | Database Connection Pooling Service | `DBCPConnectionPool` |
| PutDatabaseRecord | Table Name | `supplier_stock_nifi` |

## Permissions

NiFi runs as user 1000 inside the container. If `id -u` prints another number on Ubuntu, run
`chmod 777 ~/meridian/nifi/drops ~/meridian/nifi/landed ~/meridian/nifi/quarantine`
(the test workflow does this: its user is 1001).
