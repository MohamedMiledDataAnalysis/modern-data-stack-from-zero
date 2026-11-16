"""Chapter 32/33 — run the orders checkpoint and fail the pipeline on critical rules.

Exit code 0: every critical rule passed (warnings are printed, not fatal).
Exit code 1: at least one critical rule failed. Airflow treats that as a failed task.
"""
import sys

import great_expectations as gx

# Rules known to fail for a documented reason (Chapter 32): report, do not stop.
WARNING_ONLY = {'No order is placed before the customer signed up'}

context = gx.get_context(mode='file', project_root_dir='.')
result = context.checkpoints.get('nightly_orders').run()
run = list(result.run_results.values())[0]

critical = 0
for r in run.results:
    if r.success:
        continue
    name = r.expectation_config.description or r.expectation_config.type
    column = r.expectation_config.kwargs.get('column', '')
    if name in WARNING_ONLY:
        print(f'WARNING  {name}')
    else:
        print(f'CRITICAL {name} {column}')
        critical += 1

print(f'{critical} critical failure(s)')
sys.exit(1 if critical else 0)
