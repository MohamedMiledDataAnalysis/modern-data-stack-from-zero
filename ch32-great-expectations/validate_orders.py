"""Chapter 32 — check the Meridian orders with Great Expectations 1.x."""
import great_expectations as gx

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')

# Step 1 — a project folder that keeps every definition
context = gx.get_context(mode='file', project_root_dir='.')

# Step 2 — connect to PostgreSQL and point at the orders table
source = context.data_sources.add_or_update_postgres(name='meridian', connection_string=URL)
asset = source.add_table_asset(name='fact_orders',
                               table_name='fact_orders')
batch_def = asset.add_batch_definition_whole_table('all orders')

# Step 3 — the rules, collected in a suite
E = gx.expectations                      # a short name for the rule catalogue
suite = context.suites.add_or_update(
    gx.ExpectationSuite(name='orders_suite'))
suite.expectations = []                  # start clean when the script is rerun
suite.add_expectation(E.ExpectTableRowCountToBeBetween(
    min_value=200_000, max_value=300_000))
suite.add_expectation(E.ExpectColumnValuesToBeUnique(column='order_id'))
suite.add_expectation(E.ExpectColumnValuesToNotBeNull(column='customer_id'))
suite.add_expectation(E.ExpectColumnValuesToBeInSet(
    column='status', value_set=['completed', 'returned', 'cancelled']))
suite.add_expectation(E.ExpectColumnValuesToBeBetween(
    column='quantity', min_value=1, max_value=5))
suite.add_expectation(E.ExpectColumnValuesToBeBetween(
    column='order_date', min_value='2021-01-01', max_value='2024-01-01'))
suite.add_expectation(E.UnexpectedRowsExpectation(
    description='No order is placed before the customer signed up',
    unexpected_rows_query="""
        SELECT o.order_id, o.order_date, c.signup_date
        FROM {batch} o
        JOIN dim_customer c ON o.customer_id = c.customer_id
        WHERE o.order_date < c.signup_date"""))
suite.save()

# Step 4 — a validation: these rules, on this data
validation = context.validation_definitions.add_or_update(
    gx.ValidationDefinition(name='orders_check', data=batch_def,
                            suite=suite))
result = validation.run()

print('Success:', result.success)
for r in result.results:
    cfg = r.expectation_config
    target = cfg.kwargs.get('column') or cfg.description or ''
    count = r.result.get('unexpected_count', r.result.get('observed_value'))
    print(f"{'PASS' if r.success else 'FAIL'}  {cfg.type:<36} "
          f"{target[:22]:<22} {count}")
