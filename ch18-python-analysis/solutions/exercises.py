"""Chapter 18 — corrections (run from the ch18-python-analysis folder)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analysis import done, rfm, stats   # noqa: E402  (re-runs analysis.py)

print('\nExercise 1')
by_day = (done.assign(weekday=done['order_date'].dt.day_name())
          .groupby('weekday')['total_amount'].sum().div(1e6).round(3)
          .sort_values(ascending=False))
print(by_day)

print('\nExercise 2')
share = rfm.groupby('segment')['monetary'].sum() / rfm['monetary'].sum() * 100
print(share.round(1).sort_values(ascending=False))

print('\nExercise 3')
nl = done.loc[done['country_name'] == 'Netherlands', 'total_amount']
fr = done.loc[done['country_name'] == 'France', 'total_amount']
t = stats.ttest_ind(nl, fr, equal_var=False)
print(f'Netherlands {nl.mean():.2f}, France {fr.mean():.2f}, t = {t.statistic:.3f}, p = {t.pvalue:.4f}')

print('\nExercise 4')
r = stats.pearsonr(done['quantity'], done['total_amount'])
print(f'r = {r.statistic:.3f}, r squared = {r.statistic ** 2:.3f}')
