# Chapter 8 — Amazon S3

Start the emulator first, in its own terminal: `moto_server -p 5000`. Then, from this folder:

1. `python create_lake.py` — bucket, supplier file, 37 monthly Parquet files
2. `python read_lake.py` — read September 2023 back
3. `python lifecycle.py` — versioning, encryption, lifecycle rule
4. `python solutions/exercises.py` — corrections

For real AWS: `export MERIDIAN_S3_MODE=aws` and `export MERIDIAN_BUCKET=<your-unique-name>`.
