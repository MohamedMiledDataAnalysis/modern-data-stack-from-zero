"""Chapter 32 — corrections. Run from the ch32-great-expectations folder,
after validate_orders.py."""
import great_expectations as gx
from sqlalchemy import create_engine, text

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)
context = gx.get_context(mode='file', project_root_dir='.')
validation = context.validation_definitions.get('orders_check')

print('Exercise 1 — one bad order')
with engine.begin() as conn:
    conn.execute(text("INSERT INTO fact_orders VALUES "
                      "(250001, 1, 1, '2023-06-01', 0, 227.76, 0, 'Shipped')"))
try:
    result = validation.run(result_format='SUMMARY')
    for r in result.results:
        if not r.success and r.expectation_config.kwargs.get('column'):
            print(f"FAIL {r.expectation_config.kwargs['column']}: "
                  f"{r.result['unexpected_count']} row(s), e.g. {r.result['partial_unexpected_list']}")
finally:
    with engine.begin() as conn:
        conn.execute(text('DELETE FROM fact_orders WHERE order_id = 250001'))

print('Exercise 2 — totals must equal price x quantity')
suite = validation.suite
rule = gx.expectations.UnexpectedRowsExpectation(
    description='total_amount equals unit_price x quantity',
    unexpected_rows_query='SELECT order_id FROM {batch} '
        'WHERE total_amount <> unit_price * quantity')
suite.add_expectation(rule)
suite.save()
result = validation.run()
for r in result.results:
    d = r.expectation_config.description
    if d and 'total_amount' in d:
        print([(d, r.success)])
suite.expectations = [e for e in suite.expectations
                      if getattr(e, 'description', None) != 'total_amount equals unit_price x quantity']
suite.save()

print('Exercise 3 — the supplier stock table')
source = context.data_sources.get('meridian')
if 'supplier_stock' in [a.name for a in source.assets]:
    source.delete_asset('supplier_stock')
asset = source.add_table_asset(name='supplier_stock', table_name='supplier_stock')
batch = (asset.add_batch_definition_whole_table('all stock')
         .get_batch())
E = gx.expectations
rules = [
    E.ExpectColumnValuesToBeUnique(column='product_id'),
    E.ExpectColumnValuesToBeBetween(column='stock_qty',
                                    min_value=0),
    E.ExpectColumnValuesToBeInSet(column='reorder_level',
                                  value_set=[20, 50, 100]),
]
for exp in rules:
    r = batch.validate(exp)
    status = 'PASS' if r.success else 'FAIL'
    print(status, type(exp).__name__, exp.column)
source.delete_asset('supplier_stock')
