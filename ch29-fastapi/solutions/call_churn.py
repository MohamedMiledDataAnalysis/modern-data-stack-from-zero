"""Chapter 29, Exercise 1 — call the churn endpoint from Python.

Start the API first, from the ch29-fastapi folder:  uvicorn main:app --reload
Then, in a second terminal:                         python solutions/call_churn.py
"""
import requests

alex = {'sessions_90d': 2, 'support_tickets_90d': 3, 'days_since_login': 95,
        'newsletter_opt_in': False, 'uses_app': False}
r = requests.post('http://localhost:8000/churn', json=alex, timeout=10)
r.raise_for_status()
print(r.json()['churn_probability'])
