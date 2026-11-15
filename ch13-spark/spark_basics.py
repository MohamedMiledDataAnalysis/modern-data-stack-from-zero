"""Chapter 13, Steps 1-5 — start Spark, read the raw zone, transform, query."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

LAKE = str(Path.home() / 'meridian' / 'lake')

spark = (SparkSession.builder
         .appName('meridian')
         .master('local[*]')
         .config('spark.sql.shuffle.partitions', '4')
         .getOrCreate())
spark.sparkContext.setLogLevel('ERROR')
print('Spark', spark.version)

# Step 2 — read
orders = spark.read.parquet(f'{LAKE}/raw/orders')
orders.printSchema()
print(orders.count(), 'rows in', orders.rdd.getNumPartitions(), 'partitions')

# Step 3 — transform (lazy) then act
completed = (orders
             .filter(F.col('status') == 'completed')
             .withColumn('order_month', F.date_format('order_date', 'yyyy-MM'))
             .select('order_id', 'customer_id', 'product_id', 'order_month',
                     'total_amount', 'year'))
by_year = (completed.groupBy('year')
           .agg(F.count('*').alias('orders'),
                F.round(F.sum('total_amount'), 2).alias('revenue'))
           .orderBy('year'))
by_year.show()

# Step 4 — join a dimension
customers = spark.read.parquet(f'{LAKE}/raw/dim_customer')
countries = spark.read.parquet(f'{LAKE}/raw/dim_country')
by_country = (completed
              .join(customers, 'customer_id')
              .join(countries, 'country_id')
              .groupBy('country_name')
              .agg(F.round(F.sum('total_amount'), 2).alias('revenue'))
              .orderBy(F.desc('revenue')))
by_country.show()

# Step 5 — the same question in Spark SQL
orders.createOrReplaceTempView('orders')
customers.createOrReplaceTempView('customers')
countries.createOrReplaceTempView('countries')
spark.sql("""
    SELECT co.country_name, COUNT(*) AS returned_orders
    FROM orders o
    JOIN customers c  ON o.customer_id = c.customer_id
    JOIN countries co ON c.country_id  = co.country_id
    WHERE o.status = 'returned'
    GROUP BY co.country_name
    ORDER BY returned_orders DESC
""").show()
spark.stop()
