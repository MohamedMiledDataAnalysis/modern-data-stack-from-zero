"""Chapter 28, Exercises 1 and 2 — the app with a CSV download button and a chart by country.

Run from the ch28-streamlit folder:  streamlit run solutions/app_exercises.py
"""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
MODEL = Path(__file__).resolve().parents[2] / 'ch21-scikit-learn' / 'churn_model.joblib'

st.set_page_config(page_title='Meridian', layout='wide')


@st.cache_resource
def get_engine():
    return create_engine(URL)


@st.cache_data
def load_orders():
    return pd.read_sql("""
        SELECT o.order_date, o.status, o.total_amount::float AS amount,
               co.country_name, ca.category_name
        FROM fact_orders o
        JOIN dim_customer c  USING (customer_id)
        JOIN dim_country co  USING (country_id)
        JOIN dim_product p   USING (product_id)
        JOIN dim_category ca USING (category_id)
        WHERE o.order_date < '2024-01-01'""", get_engine(), parse_dates=['order_date'])


@st.cache_resource
def load_model():
    return joblib.load(MODEL)


orders = load_orders()
orders['month'] = orders['order_date'].dt.strftime('%Y-%m')

st.title('Meridian Retail')
tab_sales, tab_churn = st.tabs(['Sales', 'Churn risk'])

with tab_sales:
    months = sorted(orders['month'].unique(), reverse=True)
    month = st.selectbox('Month', months, index=months.index('2023-09'))
    countries = st.multiselect('Countries', sorted(orders['country_name'].unique()))

    view = orders[orders['month'] == month]
    if countries:
        view = view[view['country_name'].isin(countries)]
    done = view[view['status'] == 'completed']

    c1, c2, c3 = st.columns(3)
    c1.metric('Completed orders', f'{len(done):,}')
    c2.metric('Revenue', f'£{done["amount"].sum():,.0f}')
    c3.metric('Return rate', f'{(view["status"] == "returned").mean():.1%}')

    daily = done.groupby(done['order_date'].dt.day)['amount'].sum().rename('revenue')
    st.subheader('Revenue per day')
    st.line_chart(daily)

    st.subheader('Revenue by category')
    st.dataframe(done.groupby('category_name')['amount'].sum()
                 .sort_values(ascending=False).round(2).rename('revenue'))

    # Exercise 1 — download the category table as CSV
    by_category = (done.groupby('category_name')['amount'].sum()
                   .sort_values(ascending=False).round(2))
    st.download_button('Download as CSV', by_category.to_csv(),
                       file_name=f'meridian_categories_{month}.csv',
                       mime='text/csv')

    # Exercise 2 — completed revenue by country for the chosen month
    st.subheader('Revenue by country')
    st.bar_chart(done.groupby('country_name')['amount'].sum())

with tab_churn:
    st.write('Probability that a customer stops buying, from the Chapter 21 model.')
    sessions = st.slider('Sessions in the last 90 days', 0, 40, 12)
    tickets = st.slider('Support tickets in the last 90 days', 0, 6, 0)
    days = st.slider('Days since last login', 0, 119, 30)
    newsletter = st.checkbox('Subscribed to the newsletter')
    app = st.checkbox('Uses the mobile app')
    customer = pd.DataFrame([{'sessions_90d': sessions, 'support_tickets_90d': tickets,
                              'days_since_login': days,
                              'newsletter_opt_in': float(newsletter),
                              'uses_app': float(app)}])
    p = load_model().predict_proba(customer)[0, 1]
    st.metric('Churn probability', f'{p:.1%}')
    if p >= 0.3:
        st.warning('At risk: send a retention offer.')
    else:
        st.success('Low risk.')
