# Chapter 2 — Flat files, APIs and IoT

| File | Step |
|:--|:--|
| `make_supplier_files.py` | creates `supplier_stock.csv` and `supplier_prices.xlsx` |
| `read_csv.py`, `read_csv_pandas.py` | Steps 1–2: read and validate the CSV |
| `read_excel.py` | Step 3: read both sheets of the workbook |
| `mock_api.py` | the product API: `uvicorn mock_api:app --port 8100` |
| `call_api.py` | Steps 4–5: call the API, page by page, with a key |
| `sensor_simulator.py`, `subscriber.py` | Step 6: MQTT sensors (needs Mosquitto running) |
| `load_supplier_stock.py` | Step 7: load the valid rows into PostgreSQL |
| `solutions/` | corrections to the exercises |

Run every script from this folder, `cd ch02-files-apis-iot`, except Step 8, which runs from `sqlserver/`.

## Step 8: SQL Server as a second source

On a Mac with Apple silicon, tick *Use Rosetta for x86_64/amd64 emulation on Apple Silicon* in
Docker Desktop → Settings → General first. Microsoft does not support SQL Server under Rosetta,
and this repository's automatic tests run Step 8 on Ubuntu only. Give Docker at least 4 GB of memory.

```bash
cd sqlserver
bash start_sqlserver.sh          # SQL Server 2022 in Docker
docker logs sqlserver 2>&1 | grep "Recovery is complete"   # repeat until it prints a line
python make_purchase_orders.py   # the purchasing database meridian_erp
python read_sqlserver.py         # read it as meridian_reader, load it into PostgreSQL
docker stop sqlserver            # Chapter 12 starts it again with: docker start sqlserver
```
