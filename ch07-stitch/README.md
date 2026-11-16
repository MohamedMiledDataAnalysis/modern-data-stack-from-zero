# Chapter 7 — Stitch and the Singer standard

```bash
python tap_meridian.py --limit 2                              # look at the messages
python tap_meridian.py --limit 2500 | python target_jsonl.py  # first load
python tap_meridian.py --state state.json | python target_jsonl.py   # continue
```

```bash
python target_jsonl.py < missing_column.jsonl                 # Step 3: a record without its column
```

`missing_column.jsonl` holds a SCHEMA listing `order_id` and `status`, then a record without `status`.
`solutions/tap_products.py` is the full-table stream of Exercise 3.
