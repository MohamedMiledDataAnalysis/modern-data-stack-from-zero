"""Chapter 20, Step 6 — run the report for every month of 2023 and export HTML."""
import subprocess
from pathlib import Path

import papermill as pm

out = Path('reports')
out.mkdir(exist_ok=True)
for m in range(1, 13):
    month = f'2023-{m:02d}'
    nb = out / f'report_{month}.ipynb'
    pm.execute_notebook('monthly_report.ipynb', str(nb),
                        parameters={'month': month}, progress_bar=False)
    subprocess.run(['jupyter', 'nbconvert', '--to', 'html', '--no-input',
                    '--log-level', 'WARN', str(nb)], check=True)
    print('done', month)
print(len(list(out.glob('*.html'))), 'HTML reports in', out)
