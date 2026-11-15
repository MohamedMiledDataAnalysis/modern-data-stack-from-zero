"""Chapter 2, Step 1 — read the supplier CSV and keep only valid rows."""
import csv
from datetime import date

good, bad = [], []
seen = set()
with open('supplier_stock.csv', newline='', encoding='utf-8') as f:
    for line_no, row in enumerate(csv.DictReader(f), start=2):
        try:
            pid = int(row['product_id'])
            qty = int(row['stock_qty'])
            updated = date.fromisoformat(row['updated'])
        except ValueError as err:
            bad.append((line_no, str(err)))
            continue
        if not 1 <= pid <= 500:
            bad.append((line_no, f'unknown product_id {pid}'))
        elif pid in seen:
            bad.append((line_no, f'duplicate product_id {pid}'))
        else:
            seen.add(pid)
            good.append({'product_id': pid, 'supplier': row['supplier'],
                         'stock_qty': qty,
                         'reorder_level': int(row['reorder_level']),
                         'updated': updated})

print(f'{len(good)} valid rows, {len(bad)} rejected')
for line_no, reason in bad:
    print(f'  line {line_no}: {reason}')
