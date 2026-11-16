"""Chapter 22 — regression and time series with statsmodels."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates                                 # noqa: E402
import matplotlib.pyplot as plt                                   # noqa: E402
import pandas as pd                                               # noqa: E402
import statsmodels.formula.api as smf                             # noqa: E402
from statsmodels.tsa.arima.model import ARIMA                     # noqa: E402
from statsmodels.tsa.seasonal import seasonal_decompose           # noqa: E402
from sqlalchemy import create_engine                              # noqa: E402

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
monthly = pd.read_sql("""
    SELECT date_trunc('month', order_date)::date AS month,
           SUM(total_amount)::float / 1e6 AS revenue_m
    FROM fact_orders
    WHERE status = 'completed' AND order_date < '2024-01-01'
    GROUP BY 1 ORDER BY 1""", create_engine(URL), parse_dates=['month'])
monthly['days'] = monthly['month'].dt.days_in_month
print(monthly.head(3))

# Step 1 — does the number of days explain revenue?
ols = smf.ols('revenue_m ~ days', data=monthly).fit()
print(ols.summary().tables[1])
print(f'R-squared {ols.rsquared:.3f}')

# Step 2 — decompose the series
series = monthly.set_index('month')['revenue_m'].asfreq('MS')
parts = seasonal_decompose(series, model='additive', period=12)
print(parts.seasonal.head(12).round(3))

# Step 3 — forecast, tested on the last six months
train, test = series[:-6], series[-6:]
fit = ARIMA(train, order=(1, 0, 0), seasonal_order=(1, 0, 0, 12)).fit()
forecast = fit.forecast(6)
naive = pd.Series(train.mean(), index=test.index)
mae = (forecast - test).abs().mean()
mae_naive = (naive - test).abs().mean()
print(pd.DataFrame({'actual': test, 'forecast': forecast, 'naive': naive}).round(3))
print(f'MAE forecast {mae:.3f}  MAE naive {mae_naive:.3f}')

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(series.index, series.values, color='#14213D', label='actual')
ax.plot(forecast.index, forecast.values, color='#C9A227', marker='o', label='forecast')
ax.set_title('Completed revenue (£ million): last six months forecast')
ax.legend(frameon=False)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
fig.tight_layout()
fig.savefig('forecast.png', dpi=200)
