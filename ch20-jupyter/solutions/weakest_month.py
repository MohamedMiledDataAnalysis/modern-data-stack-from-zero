"""Exercise 3 — find the weakest month from the twelve output notebooks."""
import json
import re
from pathlib import Path

revenue = {}
for nb in sorted(Path('reports').glob('report_*.ipynb')):
    for cell in json.loads(nb.read_text())['cells']:
        for out in cell.get('outputs', []):
            text = ''.join(out.get('text', ''))
            found = re.search(r'^(\d{4}-\d{2}): .* revenue £([\d,.]+)', text)
            if found:
                revenue[found.group(1)] = float(found.group(2).replace(',', ''))

weakest = min(revenue, key=revenue.get)
print(f'{len(revenue)} reports read; weakest month {weakest}: £{revenue[weakest]:,.2f}')
