"""A minimal Singer target: reads Singer messages on stdin and writes one JSON Lines file per stream.

Writes the last STATE value to state.json, so that the next run of the tap continues from it.
"""
import json
import sys
from pathlib import Path

OUT = Path('output')
OUT.mkdir(exist_ok=True)

files, counts, schemas, state = {}, {}, {}, None
for line in sys.stdin:
    message = json.loads(line)
    kind = message['type']
    if kind == 'SCHEMA':
        schemas[message['stream']] = message['schema']
        files[message['stream']] = open(OUT / f"{message['stream']}.jsonl", 'a')
        counts[message['stream']] = 0
    elif kind == 'RECORD':
        stream = message['stream']
        if stream not in schemas:
            sys.exit(f'RECORD for {stream} arrived before its SCHEMA')
        missing = set(schemas[stream]['properties']) - set(message['record'])
        if missing:
            sys.exit(f'record {message["record"]} lacks {sorted(missing)}')
        files[stream].write(json.dumps(message['record']) + '\n')
        counts[stream] += 1
    elif kind == 'STATE':
        for f in files.values():               # data first, then the checkpoint
            f.flush()
        state = message['value']
        Path('state.json').write_text(json.dumps(state))

for stream, n in counts.items():
    print(f'{stream}: {n} records written', file=sys.stderr)
print(f'state: {json.dumps(state)}', file=sys.stderr)
