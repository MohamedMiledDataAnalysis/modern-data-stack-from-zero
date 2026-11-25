# The Modern Data Stack — Second Edition: companion repository

Code, data generator and exercise solutions for *The Modern Data Stack, Second Edition* by Mohamed Miled.

Every chapter has its own folder. Each folder holds the files you type in the chapter, in their final state, plus a `solutions/` folder with the corrections to the exercises.

## Start here

1. Follow Chapter 0 of the book to install Python 3.13, PostgreSQL, Git, Java, R and Docker Desktop.
2. Clone this repository:
   ```bash
   git clone https://github.com/MohamedMiledDataAnalysis/modern-data-stack-from-zero.git
   cd modern-data-stack-from-zero
   pip install -r requirements.txt
   ```
3. Create the Meridian Retail database (Chapter 1):
   ```bash
   python data/generate_meridian.py
   ```
   The generator uses a fixed seed (42). With the versions in `requirements.txt`, your data is identical to the data in the book: 10,000 customers, 500 products and 250,000 orders.

   The same five tables are also in `data/meridian/` as CSV files. To load the database from the files instead of generating it:
   ```bash
   python data/load_meridian_csv.py
   ```
   Both routes give identical tables; the book's automatic tests check it on every change.

## Folders

| Folder | Chapter |
|:--|:--|
| `foundations/` | Foundation 3 — the view, stored procedure and function examples, runnable after Chapter 1 |
| `data/` | Chapter 1 — the Meridian Retail generator, and the data itself as CSV files in `data/meridian/` |
| `ch00-setup/` | Chapter 0 — your machine and your tools |
| `ch01-postgresql/` | Chapter 1 — SQL databases: PostgreSQL |
| `sql-dialects/` | Interlude — SQL, one language, many dialects |
| `ch02-files-apis-iot/` | Chapter 2 — flat files, APIs and IoT streams |
| `ch03-nifi/` | Chapter 3 — Apache NiFi |
| `ch04-kafka/` | Chapter 4 — Apache Kafka |
| `ch05-airbyte/` | Chapter 5 — Airbyte |
| `ch06-fivetran/` | Chapter 6 — Fivetran |
| `ch07-stitch/` | Chapter 7 — Stitch and Singer |
| `ch08-s3/` | Chapter 8 — Amazon S3 |
| `ch09-gcs/` | Chapter 9 — Google Cloud Storage |
| `ch10-snowflake/` | Chapter 10 — Snowflake |
| `ch11-bigquery/` | Chapter 11 — BigQuery |
| `ch12-fabric/` | Chapter 12 — Microsoft Fabric |
| `ch13-spark/` | Chapter 13 — Apache Spark |
| `ch14-dbt/` | Chapter 14 — dbt |
| `ch15-databricks/` | Chapter 15 — Databricks and Delta Lake |
| `ch16-beam/` | Chapter 16 — Apache Beam |
| `ch17-pandas/` | Chapter 17 — pandas |
| `ch18-python-analysis/` | Chapter 18 — Python for analysis |
| `ch19-r/` | Chapter 19 — R for analysis |
| `ch20-jupyter/` | Chapter 20 — Jupyter |
| `ch21-scikit-learn/` | Chapter 21 — scikit-learn |
| `ch22-statsmodels/` | Chapter 22 — statsmodels |
| `ch23-tableau/` | Chapter 23 — Tableau |
| `ch24-power-bi/` | Chapter 24 — Power BI |
| `ch25-looker-studio/` | Chapter 25 — Data Studio (formerly Looker Studio) |
| `ch26-superset/` | Chapter 26 — Apache Superset |
| `ch27-excel/` | Chapter 27 — Microsoft Excel |
| `ch28-streamlit/` | Chapter 28 — Streamlit |
| `ch29-fastapi/` | Chapter 29 — FastAPI |
| `ch30-flask/` | Chapter 30 — Flask |
| `ch31-shiny/` | Chapter 31 — R Shiny |
| `ch32-great-expectations/` | Chapter 32 — Great Expectations |
| `ch33-airflow/` | Chapter 33 — Apache Airflow |
| `ch34-prometheus/` | Chapter 34 — Prometheus |
| `ch35-grafana/` | Chapter 35 — Grafana |

## How to use this repository

Type the code yourself first, from the book. Come here to compare your files with the reference, or when you are stuck. Copying files you have not typed teaches you much less.

See [TESTING.md](TESTING.md) for how each chapter was tested and which steps were written from documentation.

## Licence

- **Code**: MIT licence (see `LICENSE`). Reuse it freely in your own projects.
- **Written material** (solutions, corrections, READMEs, guides, documents and data files): © 2026 Mohamed Miled, all rights reserved, like the book *The Modern Data Stack*. Read it and study with it; do not copy, republish or sell it (see `LICENSE-TEXT.md`).
