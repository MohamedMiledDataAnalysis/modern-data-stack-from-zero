"""Chapter 21 — add a customer_engagement table with a churn label.

Each customer's website and support activity over the 90 days before
1 July 2023, and whether they stopped buying afterwards (churned).
The label follows a hidden rule plus noise, so a model has something to learn.
Seed 21 gives every reader the same table.
"""
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
rng = np.random.default_rng(21)
n = 10_000

df = pd.DataFrame({
    'customer_id': np.arange(1, n + 1),
    'sessions_90d': rng.poisson(12, n),
    'support_tickets_90d': rng.poisson(0.6, n),
    'days_since_login': rng.integers(0, 120, n),
    'newsletter_opt_in': rng.random(n) < 0.45,
    'uses_app': rng.random(n) < 0.35,
})
logit = (-1.6
         - 0.12 * df['sessions_90d']
         + 0.55 * df['support_tickets_90d']
         + 0.028 * df['days_since_login']
         - 0.6 * df['newsletter_opt_in']
         - 0.9 * df['uses_app'])
df['churned'] = rng.random(n) < 1 / (1 + np.exp(-logit))

df.to_sql('customer_engagement', create_engine(URL), if_exists='replace', index=False)
print(f"{len(df)} customers, {df['churned'].mean():.1%} churned")
