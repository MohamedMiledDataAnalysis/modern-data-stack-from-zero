# Chapter 16 — Apache Beam

Beam has its own environment: `python3.13 -m venv ~/meridian/beam-venv && source ~/meridian/beam-venv/bin/activate && pip install -r requirements.txt`

Run Chapter 13 Step 0 first (the raw zone). Then:

- `python batch_pipeline.py` — monthly revenue to `~/meridian/lake/beam/`
- `python streaming_windows.py` — one-minute windows on a replayed stream
- `python solutions/exercises.py` — corrections
