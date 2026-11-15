"""Chapter 27 — build a formatted Excel report with openpyxl."""
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from sqlalchemy import create_engine

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)
NAVY, GOLD = '14213D', 'C9A227'

monthly = pd.read_sql("""
    SELECT to_char(o.order_date, 'YYYY-MM') AS month, co.country_name,
           SUM(o.total_amount)::float AS revenue
    FROM fact_orders o
    JOIN dim_customer c USING (customer_id) JOIN dim_country co USING (country_id)
    WHERE o.status = 'completed' AND EXTRACT(YEAR FROM o.order_date) = 2023
    GROUP BY 1, 2""", engine)
pivot = monthly.pivot(index='month', columns='country_name', values='revenue')

wb = Workbook()
ws = wb.active
ws.title = 'Monthly'

# Title and header row
ws['A1'] = 'Meridian Retail: completed revenue by country, 2023 (£)'
ws['A1'].font = Font(bold=True, size=14, color=NAVY)
headers = ['Month', *pivot.columns, 'Total']
ws.append([])
ws.append(headers)
for cell in ws[3]:
    cell.font = Font(bold=True, color='FFFFFF')
    cell.fill = PatternFill('solid', fgColor=NAVY)
    cell.alignment = Alignment(horizontal='center')

# One row per month, with a SUM formula for the total
for i, (month, row) in enumerate(pivot.iterrows(), start=4):
    ws.append([month, *row.round(2).tolist()])
    last = get_column_letter(len(headers) - 1)
    ws.cell(row=i, column=len(headers), value=f'=SUM(B{i}:{last}{i})')
total_row = 4 + len(pivot)
ws.cell(row=total_row, column=1, value='Total').font = Font(bold=True)
for col in range(2, len(headers) + 1):
    letter = get_column_letter(col)
    c = ws.cell(row=total_row, column=col, value=f'=SUM({letter}4:{letter}{total_row - 1})')
    c.font = Font(bold=True)

# Formats, widths, frozen header, colour scale
for row in ws.iter_rows(min_row=4, min_col=2, max_row=total_row, max_col=len(headers)):
    for cell in row:
        cell.number_format = '#,##0'
ws.column_dimensions['A'].width = 10
for col in range(2, len(headers) + 1):
    ws.column_dimensions[get_column_letter(col)].width = 13
ws.freeze_panes = 'B4'
ws.conditional_formatting.add(
    f'B4:{get_column_letter(len(headers) - 1)}{total_row - 1}',
    ColorScaleRule(start_type='min', start_color='FFFFFF', end_type='max', end_color=GOLD))

# Line chart of the monthly total
chart = LineChart()
chart.title = 'Total completed revenue, 2023'
chart.y_axis.title = '£'
chart.height, chart.width = 7, 16
data = Reference(ws, min_col=len(headers), min_row=3, max_row=total_row - 1)
chart.add_data(data, titles_from_data=True)
chart.set_categories(Reference(ws, min_col=1, min_row=4, max_row=total_row - 1))
chart.series[0].smooth = False                 # straight lines between months
chart.legend = None                            # one series: the title says it all
ws.add_chart(chart, f'A{total_row + 2}')

# Second sheet: September's orders as an Excel table, ready for a PivotTable
sept = pd.read_sql("""
    SELECT o.order_id, o.order_date, co.country_name AS country,
           ca.category_name AS category, o.quantity, o.total_amount::float AS amount,
           o.status
    FROM fact_orders o
    JOIN dim_customer c USING (customer_id) JOIN dim_country co USING (country_id)
    JOIN dim_product p USING (product_id) JOIN dim_category ca USING (category_id)
    WHERE o.order_date >= '2023-09-01' AND o.order_date < '2023-10-01'
    ORDER BY o.order_id""", engine)
ws2 = wb.create_sheet('Orders 2023-09')
ws2.append(list(sept.columns))
for r in sept.itertuples(index=False):
    ws2.append(list(r))
table = Table(displayName='Orders202309', ref=f'A1:G{len(sept) + 1}')
table.tableStyleInfo = TableStyleInfo(name='TableStyleMedium2', showRowStripes=True)
ws2.add_table(table)
for col, width in zip('ABCDEFG', [10, 12, 13, 15, 9, 11, 11]):
    ws2.column_dimensions[col].width = width

wb.save('meridian_report_2023.xlsx')
print(f'Saved meridian_report_2023.xlsx: {len(pivot)} months x {len(pivot.columns)} countries, '
      f'{len(sept):,} September orders')
