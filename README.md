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

## Folders

| Folder | Chapter |
|:--|:--|
| `data/` | Chapter 1 — the Meridian Retail generator |
| `ch00-setup/` | Chapter 0 — your machine and your tools |
| `ch01-postgresql/` | Chapter 1 — SQL databases: PostgreSQL |
| `ch02-files-apis-iot/` | Chapter 2 — flat files, APIs and IoT streams |
| `ch14-dbt/` | Chapter 14 — dbt |

## How to use this repository

Type the code yourself first, from the book. Come here to compare your files with the reference, or when you are stuck. Copying files you have not typed teaches you much less.
