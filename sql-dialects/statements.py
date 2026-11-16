"""Splits a .sql file into statements, dropping comment lines."""


def statements(path):
    text = open(path).read()
    for chunk in text.split(';'):
        lines = [l for l in chunk.splitlines() if not l.strip().startswith('--')]
        sql = '\n'.join(lines).strip()
        if sql:
            yield sql
