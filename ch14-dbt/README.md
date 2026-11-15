# Chapter 14 — dbt

- `meridian_dbt/` — the dbt project in its final state at the end of the chapter.
- `profiles/profiles.yml` — the connection profile. Copy it to `~/.dbt/profiles.yml`.
- `solutions/` — corrections to Exercises 3 and 4.

Run the whole chapter in one go:

```bash
cd ch14-dbt/meridian_dbt
dbt build --profiles-dir ../profiles
```

Expected result: `Done. PASS=14 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=14` (8 models and 6 tests).
