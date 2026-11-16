"""Chapter 17 — corrections to Exercises 1 to 4 (run from the ch17-pandas folder)."""
from pathlib import Path

import pandas as pd

LAKE = Path.home() / 'meridian' / 'lake'
orders = pd.read_parquet(LAKE / 'cleaned' / 'orders')
products = pd.read_parquet(LAKE / 'raw' / 'dim_product')
categories = pd.read_parquet(LAKE / 'raw' / 'dim_category')

print('Exercise 1')
print(orders.query("status == 'completed'")
      .merge(products[['product_id', 'category_id']], on='product_id')
      .merge(categories, on='category_id')
      .astype({'total_amount': 'float64'})
      .groupby('category_name')['total_amount'].mean()
      .round(2).sort_values(ascending=False).head(3))

print('Exercise 2')
# the `monthly` table of Step 3: completed revenue per category and month of 2023
monthly = (orders.query("status == 'completed'")
           .merge(products[['product_id', 'category_id']], on='product_id', how='left')
           .merge(categories, on='category_id', how='left')
           .assign(month=lambda d: pd.to_datetime(d['order_date']).dt.to_period('M'))
           .loc[lambda d: d['month'].dt.year == 2023]
           .groupby(['category_name', 'month'], as_index=False)
           .agg(orders=('order_id', 'count'), revenue=('total_amount', 'sum')))
best = (monthly.groupby('month')['revenue'].sum()
        .astype(float).sort_values(ascending=False).head(1))
print(best)

print('Exercise 3')
bad = pd.concat([products, products.head(1)])
try:
    orders.merge(bad, on='product_id', validate='many_to_one')
except pd.errors.MergeError as err:
    print('MergeError:', err)

print('Exercise 4')
print(orders.merge(products[['product_id', 'category_id']], on='product_id')
      .merge(categories, on='category_id')
      .assign(returned=lambda d: d['status'] == 'returned')
      .groupby('category_name')['returned'].mean()
      .mul(100).sort_values(ascending=False).round(1).head(3))
