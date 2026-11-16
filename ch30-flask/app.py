"""Chapter 30 — a small Meridian web application with Flask.

Run from this folder:  flask --app app run --debug --port 5001
"""
from flask import Flask, abort, jsonify, render_template, request
from sqlalchemy import create_engine, text

URL = ('postgresql+psycopg2://meridian_user:meridian2024'
       '@localhost:5432/meridian_db')
engine = create_engine(URL)
app = Flask(__name__)


def monthly_revenue(year):
    with engine.connect() as conn:
        return conn.execute(text(
            "SELECT to_char(order_date, 'YYYY-MM') AS month, COUNT(*) AS orders, "
            "SUM(total_amount)::float AS revenue FROM fact_orders "
            "WHERE status = 'completed' AND EXTRACT(YEAR FROM order_date) = :y "
            "GROUP BY 1 ORDER BY 1"), {'y': year}).mappings().all()


@app.route('/')
def home():
    year = request.args.get('year', default=2023, type=int)
    rows = monthly_revenue(year)
    total = sum(r['revenue'] for r in rows)
    return render_template('home.html', year=year, rows=rows, total=total)


@app.route('/order', methods=['GET', 'POST'])
def order():
    found, order_id = None, None
    if request.method == 'POST':
        order_id = request.form.get('order_id', type=int)
        with engine.connect() as conn:
            found = conn.execute(text(
                'SELECT order_id, order_date, quantity, total_amount, status '
                'FROM fact_orders WHERE order_id = :id'), {'id': order_id}).mappings().first()
    return render_template('order.html', order_id=order_id, found=found)


@app.route('/api/revenue/<int:year>')
def api_revenue(year):
    rows = [dict(r) for r in monthly_revenue(year)]
    if not rows:
        abort(404)
    return jsonify(rows)
