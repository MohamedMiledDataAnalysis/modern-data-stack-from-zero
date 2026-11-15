"""Chapter 13 — corrections to Exercises 1 to 4 (run after spark_clean.py)."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

LAKE = str(Path.home() / 'meridian' / 'lake')
spark = (SparkSession.builder.appName('meridian-ex').master('local[*]')
         .config('spark.sql.shuffle.partitions', '4')
         .config('spark.ui.showConsoleProgress', 'false')
         .getOrCreate())
spark.sparkContext.setLogLevel('ERROR')
orders = spark.read.parquet(f'{LAKE}/cleaned/orders')

print('Exercise 1')
(orders.filter("status = 'completed'").groupBy('year')
 .agg(F.count('*').alias('orders'), F.sum('total_amount').alias('revenue'))
 .orderBy('year').show())

print('Exercise 2')
(orders.filter("status = 'completed'").groupBy('customer_id')
 .agg(F.sum('total_amount').alias('revenue'), F.count('*').alias('orders'))
 .orderBy(F.desc('revenue'), 'customer_id').limit(5).show())

print('Exercise 3')
(orders.repartition('year', 'month').write.mode('overwrite')
 .partitionBy('year', 'month').parquet(f'{LAKE}/cleaned/orders_compact'))
files = list(Path(LAKE, 'cleaned', 'orders_compact').rglob('*.parquet'))
print(len(files), 'files')

print('Exercise 4')
orders.filter('year = 2023 AND month = 9').explain()
spark.stop()
