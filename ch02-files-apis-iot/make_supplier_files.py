"""Chapter 2 — create the supplier files that Meridian receives.

Writes supplier_stock.csv (with three faulty rows, on purpose) and
supplier_prices.xlsx (two sheets). Seed 7 gives every reader the same files.
"""
import csv
import random
from datetime import date

from openpyxl import Workbook

random.seed(7)
SUPPLIERS = ['Northwind', 'Alder & Co', 'Baltic Goods']

with open('supplier_stock.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['product_id', 'supplier', 'stock_qty', 'reorder_level', 'updated'])
    for pid in range(1, 501):
        w.writerow([pid, random.choice(SUPPLIERS), random.randint(0, 400),
                    random.choice([20, 50, 100]), date(2026, 9, 22).isoformat()])
    # three faulty rows, as real supplier files contain
    w.writerow([501, 'Northwind', '', 50, '2026-09-22'])
    w.writerow([502, 'Alder & Co', 'twelve', 20, '2026-09-22'])
    w.writerow([77, 'Baltic Goods', 130, 50, '22/09/2026'])

wb = Workbook()
ws = wb.active
ws.title = 'Prices'
ws.append(['product_id', 'supplier_price_gbp', 'currency'])
for pid in range(1, 501):
    ws.append([pid, round(random.uniform(1.5, 300.0), 2), 'GBP'])
ws2 = wb.create_sheet('Contacts')
ws2.append(['supplier', 'contact', 'email'])
for s, c in zip(SUPPLIERS, ['Ana Ruiz', 'Tom Hale', 'Ieva Ozola']):
    ws2.append([s, c, s.lower().replace(' & ', '-').replace(' ', '-') + '@supplier.example'])
wb.save('supplier_prices.xlsx')
print('Wrote supplier_stock.csv (503 rows) and supplier_prices.xlsx (2 sheets)')
