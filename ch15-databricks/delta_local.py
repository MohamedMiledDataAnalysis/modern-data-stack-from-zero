"""Chapter 15, Steps 1-5 — Delta Lake on your laptop: the engine inside Databricks."""
from pathlib import Path

from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

LAKE = Path.home() / 'meridian' / 'lake'
TABLE = str(LAKE / 'delta' / 'orders')

builder = (SparkSession.builder.appName('meridian-delta').master('local[*]')
           .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension')
           .config('spark.sql.catalog.spark_catalog',
                   'org.apache.spark.sql.delta.catalog.DeltaCatalog')
           .config('spark.sql.shuffle.partitions', '4')
           .config('spark.ui.showConsoleProgress', 'false'))
spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

# Step 1 — write the cleaned orders as a Delta table (version 0)
cleaned = spark.read.parquet(str(LAKE / 'cleaned' / 'orders'))
cleaned.write.format('delta').mode('overwrite').partitionBy('year').save(TABLE)
print('version 0 rows:', spark.read.format('delta').load(TABLE).count())

# Step 2 — the transaction log
log = sorted(p.name for p in (Path(TABLE) / '_delta_log').glob('*.json'))
print('log files:', log)

# Step 3 — MERGE: three orders change status, one new order arrives (version 1)
changes = spark.createDataFrame(
    [(1, 'returned'), (2, 'returned'), (3, 'cancelled')], ['order_id', 'new_status'])
target = DeltaTable.forPath(spark, TABLE)
(target.alias('t')
 .merge(changes.alias('c'), 't.order_id = c.order_id')
 .whenMatchedUpdate(set={'status': 'c.new_status'})
 .execute())
new = (spark.read.format('delta').load(TABLE).filter('order_id = 4')
       .withColumn('order_id', F.lit(250001).cast('long'))
       .withColumn('order_date', F.to_date(F.lit('2024-01-02'))))
(target.alias('t').merge(new.alias('n'), 't.order_id = n.order_id')
 .whenNotMatchedInsertAll().execute())

now = spark.read.format('delta').load(TABLE)
print('now rows:', now.count())
now.filter('order_id <= 3').select('order_id', 'status').orderBy('order_id').show()

# Step 4 — history and time travel
target.history().select('version', 'operation', 'operationMetrics.numTargetRowsUpdated',
                        'operationMetrics.numTargetRowsInserted').orderBy('version').show(truncate=False)
v0 = spark.read.format('delta').option('versionAsOf', 0).load(TABLE)
v0.filter('order_id <= 3').select('order_id', 'status').orderBy('order_id').show()

# Step 5 — schema enforcement
bad = now.limit(1).withColumn('total_amount', F.lit('a lot'))
try:
    bad.write.format('delta').mode('append').save(TABLE)
except Exception as err:
    print('Refused:', type(err).__name__, str(err).splitlines()[0][:160])
spark.stop()
