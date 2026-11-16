# Chapter 6 — Fivetran

Fivetran runs in its own cloud. To practise the queries without an account:

```bash
psql -h localhost -U meridian_user meridian_db -f simulate_destination.sql   # builds meridian_public with Fivetran system columns
psql -h localhost -U meridian_user meridian_db -f queries.sql
python solutions/mar_estimate.py
```

Remove the simulation with `DROP SCHEMA meridian_public CASCADE;`.
