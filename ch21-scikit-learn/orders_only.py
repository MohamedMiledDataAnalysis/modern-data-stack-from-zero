"""Chapter 21, Step 1 — can order history alone predict churn?"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
o = pd.read_sql('SELECT customer_id, order_date, status, total_amount::float AS amount '
                'FROM fact_orders', create_engine(URL), parse_dates=['order_date'])
cut = pd.Timestamp('2023-07-01')
past = o[o['order_date'] < cut]
after = o[(o['order_date'] >= cut) & (o['status'] == 'completed')]

X = past.groupby('customer_id').agg(
    orders=('amount', 'size'), spend=('amount', 'sum'),
    return_rate=('status', lambda s: (s == 'returned').mean()),
    recency=('order_date', lambda d: (cut - d.max()).days))
y = ~X.index.isin(after['customer_id'])
print(f'{y.mean():.1%} of customers bought nothing after 1 July 2023')

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=300, min_samples_leaf=20,
                               random_state=42).fit(X_train, y_train)
print('ROC AUC on unseen customers:',
      round(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]), 3))
