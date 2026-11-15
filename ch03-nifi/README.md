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
| both PutFile | failure | retry |
