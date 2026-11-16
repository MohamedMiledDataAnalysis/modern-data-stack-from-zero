"""Runs sparksql.sql on local Spark, with the Meridian tables read from PostgreSQL."""
from decimal import Decimal

import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.types import (DateType, DecimalType, IntegerType, StringType, StructField,
                               StructType)

from statements import statements

spark = (SparkSession.builder.master('local[*]').appName('dialects')
         .config('spark.sql.shuffle.partitions', '4')
         .config('spark.ui.showConsoleProgress', 'false').getOrCreate())
spark.sparkContext.setLogLevel('ERROR')

TYPES = {'integer': IntegerType(), 'date': DateType(), 'numeric': DecimalType(10, 2),
         'character varying': StringType(), 'text': StringType()}
conn = psycopg2.connect(host='localhost', dbname='meridian_db',
                        user='meridian_user', password='meridian2024')
cur = conn.cursor()
for table in ('fact_orders', 'dim_customer', 'dim_product'):
    cur.execute("SELECT column_name, data_type FROM information_schema.columns "
                "WHERE table_name = %s ORDER BY ordinal_position", (table,))
    schema = StructType([StructField(c, TYPES[t]) for c, t in cur.fetchall()])
    cur.execute(f'SELECT * FROM {table}')
    spark.createDataFrame(cur.fetchall(), schema).createOrReplaceTempView(table)

for sql in statements('sparksql.sql'):
    spark.sql(sql).show(truncate=False)
