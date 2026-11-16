# Chapter 7 — Stitch and the Singer standard

```bash
python tap_meridian.py --limit 2                              # look at the messages
python tap_meridian.py --limit 2500 | python target_jsonl.py  # first load
python tap_meridian.py --state state.json | python target_jsonl.py   # continue
```

`solutions/tap_products.py` is the full-table stream of Exercise 3.
