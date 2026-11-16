"""Chapter 15 — corrections (run after delta_local.py)."""
from pathlib import Path

from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable
from pyspark.sql import SparkSession

TABLE = str(Path.home() / 'meridian' / 'lake' / 'delta' / 'orders')
builder = (SparkSession.builder.appName('meridian-delta-ex').master('local[*]')
           .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension')
           .config('spark.sql.catalog.spark_catalog',
                   'org.apache.spark.sql.delta.catalog.DeltaCatalog')
           .config('spark.ui.showConsoleProgress', 'false'))
spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

print('Exercise 1 — returned orders in version 0 and now')
for v in (0, None):
    reader = spark.read.format('delta')
    if v is not None:
        reader = reader.option('versionAsOf', v)
    n = reader.load(TABLE).filter("status = 'returned'").count()
    print('version 0' if v == 0 else 'current  ', n)

print('Exercise 2 — SQL on the Delta table')
spark.sql(f"""
    SELECT year, COUNT(*) AS orders
    FROM delta.`{TABLE}` VERSION AS OF 0
    GROUP BY year ORDER BY year
""").show()

print('Exercise 3 — restore version 0')
DeltaTable.forPath(spark, TABLE).restoreToVersion(0)
print('rows after restore:', spark.read.format('delta').load(TABLE).count())
DeltaTable.forPath(spark, TABLE).history().select('version', 'operation').orderBy('version').show()
spark.stop()
