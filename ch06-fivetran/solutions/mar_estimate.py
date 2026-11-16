"""Exercise 4 - estimate Meridian's monthly active rows (MAR) for one month."""
DAYS = 30
new_orders = 100 * 24 * DAYS                 # 100 new orders an hour
changed_orders = 40 * DAYS                   # 40 orders a day change status
new_customers = 20 * DAYS                    # 20 sign-ups a day
price_changes = 500                          # every product repriced once

mar = {
    'fact_orders': new_orders + changed_orders,
    'dim_customer': new_customers,
    'dim_product': price_changes,
}
for table, rows in mar.items():
    print(f'{table:<13}{rows:>8,}')
total = sum(mar.values())
print(f"{'total':<13}{total:>8,}")
print(f'share of the Free plan (500,000 MAR): {total / 500_000:.1%}')
