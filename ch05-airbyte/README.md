# Chapter 5 — Airbyte

- `sync_via_api.py` — creates, through Airbyte's API, the source `Meridian PostgreSQL`,
  the destination `Meridian raw (PostgreSQL)` (schema `airbyte_raw`) and the connection
  `Meridian to raw` (`dim_product` full refresh overwrite, `fact_orders` incremental append
  on `order_id`), runs the first sync, inserts orders 250001 to 250003, and runs the second sync.

Run it on a fresh Airbyte, instead of Steps 3 to 7 of the chapter (not in addition):

```bash
abctl local credentials          # copy Client-Id and Client-Secret
python sync_via_api.py <Client-Id> <Client-Secret> <address of your machine, Step 2>
```

Afterwards, delete the three test orders: `DELETE FROM fact_orders WHERE order_id > 250000;`
