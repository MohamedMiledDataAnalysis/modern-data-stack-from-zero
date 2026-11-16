"""Runs snowflake.sql on fakesnow, after Chapter 10's load_snowflake.py.
Run from this folder, in Chapter 10's environment (snowflake-venv)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ch10-snowflake'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ch10-snowflake'))
from sf_config import sf_connect                      # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from statements import statements                     # noqa: E402

cur = sf_connect().cursor()
here = os.path.dirname(os.path.abspath(__file__))
for sql in statements(os.path.join(here, 'snowflake.sql')):
    cur.execute(sql)
    print([d[0] for d in cur.description])
    for row in cur.fetchall():
        print(row)
    print()
