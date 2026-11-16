# Chapter 29 — FastAPI

Run Chapter 21 first (`churn_model.joblib`). Then, from this folder:

- `uvicorn main:app --reload` — documentation at http://localhost:8000/docs
- `python solutions/call_churn.py` — Exercise 1 (with the API running)
- `uvicorn solutions.main_secure:app --reload` — Exercise 2 (key required on /churn)
- `python -m pytest solutions/test_main.py -q` — Exercise 3
