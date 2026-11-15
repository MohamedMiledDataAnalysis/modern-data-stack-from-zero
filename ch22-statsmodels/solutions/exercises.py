"""Chapter 22 — corrections (run from the ch22-statsmodels folder)."""
import sys
from pathlib import Path

import statsmodels.formula.api as smf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from model import monthly, test   # noqa: E402  (re-runs model.py)

print('\nExercise 1')
train_df, test_df = monthly.iloc[:-6], monthly.iloc[-6:]
days_model = smf.ols('revenue_m ~ days', data=train_df).fit()
pred = days_model.predict(test_df)
print(f'MAE days model {(pred.values - test.values).__abs__().mean():.3f}')

print('\nExercise 2')
m = monthly.assign(per_day=monthly['revenue_m'] / monthly['days'] * 1e3,
                   t=range(len(monthly)))
trend = smf.ols('per_day ~ t', data=m).fit()
print(f"slope {trend.params['t']:.3f} thousand £ per day per month, p = {trend.pvalues['t']:.3f}")
