"""Chapter 21 — corrections (run from the ch21-scikit-learn folder, after train.py)."""
import joblib
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
df = pd.read_sql('SELECT * FROM customer_engagement', create_engine(URL))
FEATURES = ['sessions_90d', 'support_tickets_90d', 'days_since_login',
            'newsletter_opt_in', 'uses_app']
X, y = df[FEATURES].astype(float), df['churned']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
pipe = joblib.load('churn_model.joblib')
proba = pipe.predict_proba(X_test)[:, 1]

print('Exercise 1')
for threshold in (0.5, 0.3):
    pred = proba >= threshold
    print(f'threshold {threshold}: recall {recall_score(y_test, pred):.3f}, '
          f'precision {precision_score(y_test, pred):.3f}')
print(confusion_matrix(y_test, proba >= 0.3))

print('Exercise 2')
alex = pd.DataFrame([{'sessions_90d': 2, 'support_tickets_90d': 3, 'days_since_login': 95,
                      'newsletter_opt_in': 0.0, 'uses_app': 0.0}])
print('churn probability:', round(pipe.predict_proba(alex)[0, 1], 3))

print('Exercise 3')
fewer = [f for f in FEATURES if f != 'days_since_login']
pipe.fit(X_train[fewer], y_train)
print('AUC without days_since_login:',
      round(roc_auc_score(y_test, pipe.predict_proba(X_test[fewer])[:, 1]), 3))
