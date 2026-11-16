"""Chapter 32, Step 5 — a checkpoint that validates and publishes Data Docs."""
import great_expectations as gx

context = gx.get_context(mode='file', project_root_dir='.')
validation = context.validation_definitions.get('orders_check')
checkpoint = context.checkpoints.add_or_update(gx.Checkpoint(
    name='nightly_orders',
    validation_definitions=[validation],
    actions=[gx.checkpoint.UpdateDataDocsAction(name='docs')],
    result_format={'result_format': 'COMPLETE'}))

result = checkpoint.run()
print('Checkpoint success:', result.success)
run = list(result.run_results.values())[0]
failed = [r for r in run.results if not r.success][0]
print('Failed rule:', failed.expectation_config.description)
print('Rows breaking it:', failed.result['observed_value'])
for row in failed.result['details']['unexpected_rows'][:3]:
    print('  ', row)
docs = context.get_docs_sites_urls()[0]['site_url']
print('Data Docs:', docs.replace(context.root_directory, '.'))
