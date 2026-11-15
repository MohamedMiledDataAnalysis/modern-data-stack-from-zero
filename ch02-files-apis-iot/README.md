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

Run every script from this folder: `cd ch02-files-apis-iot`.
