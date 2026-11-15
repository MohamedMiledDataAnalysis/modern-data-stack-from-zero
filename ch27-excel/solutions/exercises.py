"""Chapter 27 — corrections. Run from the ch27-excel folder, after build_report.py."""
import pandas as pd
from openpyxl import load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Font
from sqlalchemy import create_engine

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)
GOLD = 'C9A227'
wb = load_workbook('meridian_report_2023.xlsx')

# Exercise 1 — a category sheet with a bar chart
by_cat = pd.read_sql("""
    SELECT ca.category_name AS category, SUM(o.total_amount)::float AS revenue
    FROM fact_orders o JOIN dim_product p USING (product_id)
    JOIN dim_category ca USING (category_id)
    WHERE o.status = 'completed' AND EXTRACT(YEAR FROM o.order_date) = 2023
    GROUP BY 1 ORDER BY 2 DESC""", engine)
ws3 = wb.create_sheet('Categories')
ws3.append(['Category', 'Revenue'])
for r in by_cat.itertuples(index=False):
    ws3.append([r.category, round(r.revenue, 2)])
for (cell,) in ws3.iter_rows(min_row=2, min_col=2, max_col=2):
    cell.number_format = '#,##0'
bars = BarChart()
bars.type = 'bar'
bars.add_data(Reference(ws3, min_col=2, min_row=1, max_row=13), titles_from_data=True)
bars.set_categories(Reference(ws3, min_col=1, min_row=2, max_row=13))
bars.legend = None
ws3.add_chart(bars, 'D2')
print('Exercise 1: top category', by_cat.iloc[0]['category'], round(by_cat.iloc[0]['revenue'], 2))

# Exercise 2 — the best month of each country in bold gold
ws = wb['Monthly']
for col in 'BCDEFG':
    rng = f'{col}4:{col}15'
    ws.conditional_formatting.add(rng, FormulaRule(
        formula=[f'{col}4=MAX(${col}$4:${col}$15)'], font=Font(bold=True, color=GOLD)))
wb.save('meridian_report_2023_ex.xlsx')
print('Exercise 2: saved meridian_report_2023_ex.xlsx')

# Exercise 3 — check the workbook against the database
monthly = pd.read_excel('meridian_report_2023.xlsx', sheet_name='Monthly',
                        skiprows=2, nrows=12)
countries = ['France', 'Germany', 'Italy', 'Netherlands', 'Spain', 'UK']
print(monthly[['Month', 'France', 'UK']].head(3))
print('Exercise 3:', round(monthly[countries].sum().sum(), 2))
