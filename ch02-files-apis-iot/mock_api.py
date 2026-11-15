"""Chapter 2 — a small product API in front of the Meridian database.

Start it with:  uvicorn mock_api:app --port 8100
Every request needs the header  X-API-Key: meridian-demo-key
"""
from fastapi import FastAPI, Header, HTTPException, Query
from sqlalchemy import create_engine, text

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)
API_KEY = 'meridian-demo-key'
app = FastAPI(title='Meridian Product API')


def check_key(key):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail='Invalid or missing API key')


@app.get('/v1/products/{product_id}')
def get_product(product_id: int, x_api_key: str | None = Header(default=None)):
    check_key(x_api_key)
    with engine.connect() as conn:
        row = conn.execute(text(
            'SELECT p.product_id, p.product_name, c.category_name, p.unit_price '
            'FROM dim_product p JOIN dim_category c USING (category_id) '
            'WHERE p.product_id = :pid'), {'pid': product_id}).mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return {**row, 'unit_price': float(row['unit_price'])}


@app.get('/v1/products')
def list_products(page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=100),
                  x_api_key: str | None = Header(default=None)):
    check_key(x_api_key)
    with engine.connect() as conn:
        total = conn.execute(text('SELECT COUNT(*) FROM dim_product')).scalar()
        rows = conn.execute(text(
            'SELECT product_id, product_name, category_id, unit_price '
            'FROM dim_product ORDER BY product_id LIMIT :n OFFSET :o'),
            {'n': page_size, 'o': (page - 1) * page_size}).mappings().all()
    items = [{**r, 'unit_price': float(r['unit_price'])} for r in rows]
    return {'page': page, 'page_size': page_size, 'total': total,
            'next_page': page + 1 if page * page_size < total else None,
            'items': items}
