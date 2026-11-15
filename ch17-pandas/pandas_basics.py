"""Chapter 17 — pandas on the Meridian cleaned zone."""
from pathlib import Path

import pandas as pd

LAKE = Path.home() / 'meridian' / 'lake'

# Step 1 — read
orders = pd.read_parquet(LAKE / 'cleaned' / 'orders')
products = pd.read_parquet(LAKE / 'raw' / 'dim_product')
categories = pd.read_parquet(LAKE / 'raw' / 'dim_category')
print(orders.shape)
print(orders.dtypes)
print(orders.memory_usage(deep=True).sum() / 1e6, 'MB')

# Step 2 — select and filter
done = orders.loc[orders['status'] == 'completed',
                  ['order_id', 'product_id', 'order_date', 'quantity', 'total_amount']]
print(len(done), 'completed orders')

# Step 3 — a method chain: completed revenue by category and month, 2023
monthly = (
    orders
    .query("status == 'completed'")
    .merge(products[['product_id', 'category_id']], on='product_id', how='left')
    .merge(categories, on='category_id', how='left')
    .assign(month=lambda d: pd.to_datetime(d['order_date']).dt.to_period('M'))
    .loc[lambda d: d['month'].dt.year == 2023]
    .groupby(['category_name', 'month'], as_index=False)
    .agg(orders=('order_id', 'count'), revenue=('total_amount', 'sum'))
    .sort_values(['category_name', 'month'])
)
print(monthly.head(3))
print(len(monthly), 'rows')

# Step 4 — pivot: one row per category, one column per quarter
pivot = (monthly
         .assign(quarter=lambda d: d['month'].dt.quarter)
         .pivot_table(index='category_name', columns='quarter',
                      values='revenue', aggfunc='sum')
         .astype(float).round(0))
print(pivot.head(4))
