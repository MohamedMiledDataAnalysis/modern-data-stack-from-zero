"""Chapter 17, Step 7 — the same question on growing data, three ways.

    python size_test.py pandas        # read every column, as Step 1 did
    python size_test.py pandas-lean   # read three columns, with Arrow types
    python size_test.py spark         # Spark, as in Chapter 13

Question: completed revenue by year, on ~/meridian/lake/scaled/orders
(build it first with ../data/scale_up.py). Each run prints the answer,
the time it took and the most memory Python used.
"""
import resource
import sys
import time
from pathlib import Path

DATA = Path.home() / 'meridian' / 'lake' / 'scaled' / 'orders'
engine = sys.argv[1]
start = time.perf_counter()

if engine in ('pandas', 'pandas-lean'):
    import pandas as pd
    if engine == 'pandas':
        orders = pd.read_parquet(DATA)
    else:
        orders = pd.read_parquet(DATA, columns=['year', 'total_amount', 'status'],
                                 dtype_backend='pyarrow')
    print(f'{len(orders):,} rows, {orders.memory_usage(deep=True).sum() / 1e6:,.0f} MB in memory')
    done = orders[orders['status'] == 'completed']
    result = (done.astype({'total_amount': 'float64'})
                  .groupby('year')['total_amount'].sum().round(2))
    print(result.to_string())
elif engine == 'spark':
    from pyspark.sql import SparkSession, functions as F
    spark = (SparkSession.builder.master('local[*]').appName('size_test')
             .config('spark.sql.shuffle.partitions', '4')
             .config('spark.ui.showConsoleProgress', 'false').getOrCreate())
    spark.sparkContext.setLogLevel('ERROR')
    orders = spark.read.parquet(str(DATA))
    print(f'{orders.count():,} rows')
    (orders.filter(F.col('status') == 'completed')
           .groupBy('year').agg(F.round(F.sum('total_amount'), 2).alias('total_amount'))
           .orderBy('year').show())
    gateway = spark.sparkContext._gateway
    spark.stop()
    gateway.shutdown()
    gateway.proc.stdin.close()      # Java stops when this pipe closes; then its memory can be read
    gateway.proc.wait(timeout=60)
else:
    sys.exit('engine must be pandas, pandas-lean or spark')

seconds = time.perf_counter() - start
unit = 1e6 if sys.platform == 'darwin' else 1e3     # ru_maxrss: bytes on macOS, KB on Linux
python_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / unit
print(f'{engine}: {seconds:.1f} s, peak memory: Python {python_mb:,.0f} MB', end='')
if engine == 'spark':
    java_mb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / unit
    print(f', Java {java_mb:,.0f} MB', end='')
print()
