"""Chapter 21, Steps 2-6 — train, evaluate, tune and save a churn model."""
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
df = pd.read_sql('SELECT * FROM customer_engagement', create_engine(URL))
FEATURES = ['sessions_90d', 'support_tickets_90d', 'days_since_login',
            'newsletter_opt_in', 'uses_app']
X, y = df[FEATURES].astype(float), df['churned']

# Step 2 — split once, keep the test set aside
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
print(len(X_train), 'training rows,', len(X_test), 'test rows')

# Step 3 — a baseline: always predict "stays"
print('Accuracy of always saying "stays":', round(1 - y_test.mean(), 3))

# Step 4 — a pipeline: scale, then logistic regression
pipe = Pipeline([('scale', StandardScaler()),
                 ('model', LogisticRegression(max_iter=1000))])
pipe.fit(X_train, y_train)
proba = pipe.predict_proba(X_test)[:, 1]
print('Logistic regression ROC AUC:', round(roc_auc_score(y_test, proba), 3))
print(classification_report(y_test, pipe.predict(X_test), digits=3))

# Step 5 — try a forest, tuned with cross-validation
grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    {'n_estimators': [200, 400], 'max_depth': [4, 8, None],
     'min_samples_leaf': [1, 20]},
    scoring='roc_auc', cv=5, n_jobs=-1)
grid.fit(X_train, y_train)
print('Best forest:', grid.best_params_, 'CV AUC', round(grid.best_score_, 3))
print('Forest ROC AUC on test:',
      round(roc_auc_score(y_test, grid.predict_proba(X_test)[:, 1]), 3))

# Step 6 — what drives churn, and save the model
coefs = pd.Series(pipe.named_steps['model'].coef_[0], index=FEATURES).round(3)
print(coefs.sort_values())
joblib.dump(pipe, 'churn_model.joblib')
print('Saved churn_model.joblib')
