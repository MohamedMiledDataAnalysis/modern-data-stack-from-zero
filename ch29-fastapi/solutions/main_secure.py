"""Chapter 29, Exercise 2 — the Meridian API with a key required on /churn.

Run from the ch29-fastapi folder:  uvicorn solutions.main_secure:app --reload
Documentation:         http://localhost:8000/docs
"""
import os
from pathlib import Path

import joblib
import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
MODEL = Path(__file__).resolve().parents[2] / 'ch21-scikit-learn' / 'churn_model.joblib'

engine = create_engine(URL)
model = joblib.load(MODEL)
app = FastAPI(title='Meridian API', version='1.0')
API_KEY = os.environ.get('MERIDIAN_API_KEY', 'change-me')


def require_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail='Invalid or missing API key')


class Order(BaseModel):
    order_id: int
    customer_id: int
    order_date: str
    total_amount: float
    status: str


class Customer(BaseModel):
    sessions_90d: int = Field(ge=0, description='Website sessions, last 90 days')
    support_tickets_90d: int = Field(ge=0)
    days_since_login: int = Field(ge=0, le=365)
    newsletter_opt_in: bool
    uses_app: bool


class ChurnScore(BaseModel):
    churn_probability: float
    at_risk: bool


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/orders/{order_id}', response_model=Order)
def get_order(order_id: int):
    with engine.connect() as conn:
        row = conn.execute(text(
            'SELECT order_id, customer_id, order_date::text, total_amount::float, status '
            'FROM fact_orders WHERE order_id = :id'), {'id': order_id}).mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail=f'Order {order_id} not found')
    return row


@app.get('/revenue')
def revenue(month: str = Query(pattern=r'^\d{4}-\d{2}$', examples=['2023-09'])):
    with engine.connect() as conn:
        row = conn.execute(text(
            "SELECT COUNT(*) AS orders, COALESCE(SUM(total_amount), 0)::float AS revenue "
            "FROM fact_orders WHERE status = 'completed' "
            "AND to_char(order_date, 'YYYY-MM') = :m"), {'m': month}).mappings().first()
    return {'month': month, **row}


@app.post('/churn', response_model=ChurnScore, dependencies=[Depends(require_key)])
def churn(customer: Customer):
    features = pd.DataFrame([customer.model_dump()]).astype(float)
    p = float(model.predict_proba(features)[0, 1])
    return ChurnScore(churn_probability=round(p, 4), at_risk=p >= 0.3)
