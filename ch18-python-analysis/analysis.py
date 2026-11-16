"""Chapter 18 — analysing Meridian with Python: statistics, trends, RFM, tests."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')                       # draw to files, no window needed
import matplotlib.dates as mdates           # noqa: E402
import matplotlib.pyplot as plt             # noqa: E402
import pandas as pd                         # noqa: E402
from scipy import stats                     # noqa: E402
from sqlalchemy import create_engine        # noqa: E402

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)
orders = pd.read_sql("""
    SELECT o.order_id, o.customer_id, o.order_date, o.quantity,
           o.total_amount::float AS total_amount, o.status, co.country_name
    FROM fact_orders o
    JOIN dim_customer c  ON o.customer_id = c.customer_id
    JOIN dim_country co ON c.country_id  = co.country_id
""", engine, parse_dates=['order_date'])
done = orders[orders['status'] == 'completed']

# Step 1 — describe
print(done['total_amount'].describe().round(2))

# Step 2 — monthly trend, saved as a chart
monthly = (done[done['order_date'] < '2024-01-01']
           .set_index('order_date')['total_amount']
           .resample('MS').sum() / 1e6)
fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(monthly.index, monthly.values, color='#14213D')
ax.set_title('Meridian completed revenue per month (£ million)')
ax.set_ylim(2.5, 3.3)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
fig.tight_layout()
fig.savefig('monthly_revenue.png', dpi=200)
print('lowest month:', monthly.idxmin().strftime('%Y-%m'), round(monthly.min(), 3))
print('highest month:', monthly.idxmax().strftime('%Y-%m'), round(monthly.max(), 3))

# Step 3 — RFM segmentation
today = pd.Timestamp('2024-01-02')
rfm = done.groupby('customer_id').agg(
    recency=('order_date', lambda d: (today - d.max()).days),
    frequency=('order_id', 'count'),
    monetary=('total_amount', 'sum'))
rfm['R'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)


def segment(row):
    if row.R >= 4 and row.F >= 4 and row.M >= 4:
        return 'Champions'
    if row.R <= 2 and row.F >= 4:
        return 'At risk'
    if row.R <= 2 and row.F <= 2:
        return 'Lost'
    return 'Regular'


rfm['segment'] = rfm.apply(segment, axis=1)
print(rfm['segment'].value_counts())

# Step 4 — is the average basket in Spain different from the UK?
uk = done.loc[done['country_name'] == 'UK', 'total_amount']
es = done.loc[done['country_name'] == 'Spain', 'total_amount']
t = stats.ttest_ind(es, uk, equal_var=False)
print(f'Spain mean {es.mean():.2f}, UK mean {uk.mean():.2f}, '
      f't = {t.statistic:.3f}, p = {t.pvalue:.4f}')

# Step 5 — correlation
print(done[['quantity', 'total_amount']].corr().round(3))
