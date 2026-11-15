"""Chapter 1 — connect to Meridian Retail from Python."""
import pandas as pd
from sqlalchemy import create_engine, text

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)

with engine.connect() as conn:
    n = conn.execute(text('SELECT COUNT(*) FROM fact_orders')).scalar()
print(f'fact_orders holds {n:,} rows')

df = pd.read_sql('SELECT status, COUNT(*) AS orders FROM fact_orders '
                 'GROUP BY status ORDER BY orders DESC', engine)
print(df)
