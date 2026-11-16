# Chapter 12 - the cells of the Fabric notebook "meridian_lakehouse".
# In Fabric, `spark` already exists and the lakehouse is attached: paths start with Files/.
# Locally (python notebook/meridian_lakehouse.py), the same code runs on the files in ./upload.
import os

try:
    spark                                                         # noqa: F821 - exists in Fabric
    BASE = 'Files/meridian'
except NameError:
    from pyspark.sql import SparkSession
    spark = (SparkSession.builder.master('local[*]').appName('fabric-local')
             .config('spark.sql.shuffle.partitions', '4')
             .config('spark.ui.showConsoleProgress', 'false').getOrCreate())
    spark.sparkContext.setLogLevel('ERROR')
    BASE = os.path.abspath('upload')

from pyspark.sql import functions as F

# Cell 1 - turn each uploaded file into a table
for name in ['dim_country', 'dim_category', 'dim_customer', 'dim_product', 'fact_orders']:
    df = spark.read.parquet(f'{BASE}/{name}.parquet')
    df.write.mode('overwrite').saveAsTable(name)
    print(name, df.count())

# Cell 2 - a gold table: completed revenue per month and country
monthly = (spark.table('fact_orders').filter(F.col('status') == 'completed')
           .join(spark.table('dim_customer'), 'customer_id')
           .join(spark.table('dim_country'), 'country_id')
           .groupBy(F.date_trunc('month', 'order_date').cast('date').alias('month'),
                    'country_name')
           .agg(F.count('*').alias('orders'),
                F.sum('total_amount').alias('revenue')))
monthly.write.mode('overwrite').saveAsTable('gold_monthly_revenue')

# Cell 3 - check
spark.sql("""
    SELECT month, country_name, orders, revenue
    FROM gold_monthly_revenue
    WHERE month = DATE '2023-09-01'
    ORDER BY revenue DESC
""").show()
