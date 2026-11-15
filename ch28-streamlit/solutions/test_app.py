"""Exercise 3 — test the app without a browser, with Streamlit's AppTest.

Run from the ch28-streamlit folder:  python -m pytest solutions/test_app.py -q
"""
from streamlit.testing.v1 import AppTest


def metrics(at):
    return {m.label: m.value for m in at.metric}


def test_september_2023():
    at = AppTest.from_file('../app.py', default_timeout=60).run()
    assert not at.exception
    assert metrics(at)['Completed orders'] == '4,161'
    assert metrics(at)['Revenue'] == '£2,945,520'


def test_france_in_february():
    at = AppTest.from_file('../app.py', default_timeout=60).run()
    at.selectbox[0].set_value('2023-02').run()
    at.multiselect[0].set_value(['France']).run()
    assert metrics(at)['Completed orders'] == '618'


def test_alex_is_at_risk():
    at = AppTest.from_file('../app.py', default_timeout=60).run()
    at.slider[0].set_value(2).run()
    at.slider[1].set_value(3).run()
    at.slider[2].set_value(95).run()
    assert metrics(at)['Churn probability'] == '92.2%'
    assert at.warning[0].value == 'At risk: send a retention offer.'
