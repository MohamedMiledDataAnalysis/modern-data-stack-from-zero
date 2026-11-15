"""Chapter 13, Step 6 — clean the raw orders and write the cleaned zone."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

LAKE = str(Path.home() / 'meridian' / 'lake')
spark = (SparkSession.builder.appName('meridian-clean').master('local[*]')
         .config('spark.sql.shuffle.partitions', '4')
         .config('spark.ui.showConsoleProgress', 'false')
         .getOrCreate())
spark.sparkContext.setLogLevel('ERROR')

raw = spark.read.parquet(f'{LAKE}/raw/orders')
cleaned = (raw
           .dropDuplicates(['order_id'])
           .withColumn('order_date', F.to_date('order_date'))
           .withColumn('unit_price', F.col('unit_price').cast('decimal(8,2)'))
           .withColumn('total_amount', F.col('total_amount').cast('decimal(10,2)'))
           .withColumn('status', F.lower(F.trim('status')))
           .withColumn('cleaned_at', F.current_timestamp()))

cleaned.explain()
(cleaned.write.mode('overwrite')
 .partitionBy('year', 'month')
 .parquet(f'{LAKE}/cleaned/orders'))

back = spark.read.parquet(f'{LAKE}/cleaned/orders')
print(back.count(), 'rows written')
back.filter('year = 2023 AND month = 9').groupBy('status') \
    .agg(F.count('*').alias('orders'), F.sum('total_amount').alias('revenue')) \
    .orderBy('status').show()
spark.stop()
