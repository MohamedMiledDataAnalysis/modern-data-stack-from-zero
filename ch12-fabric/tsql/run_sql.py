"""Runs each statement of a .sql file on the local SQL Server and prints the results."""
import sys

import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('mssql+pymssql://sa:Meridian2026!@localhost:1433/meridian')
script = open(sys.argv[1]).read()
for statement in [s for s in script.split(';') if s.strip()]:
    lines = [l for l in statement.splitlines() if not l.strip().startswith('--')]
    if not ''.join(lines).strip():
        continue
    with engine.connect() as conn:
        df = pd.read_sql(text('\n'.join(lines)), conn)
    print(df.to_string(index=False), '\n')
