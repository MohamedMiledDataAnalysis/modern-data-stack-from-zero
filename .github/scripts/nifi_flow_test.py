"""Builds the flow of Chapter 3 through NiFi's REST API, with the settings the book gives,
drops the supplier file and checks the 500 valid / 3 rejected split.

Every property is set by the label the reader sees in NiFi's dialogue (its display name),
and every choice by its displayed value, so the test follows the book's clicks.
Used only by .github/workflows/ch03-nifi.yml.
"""
import glob
import json
import os
import shutil
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()
API = 'https://localhost:8443/nifi-api'
DATA = os.path.expanduser('~/meridian/nifi')
REPO = os.environ.get('GITHUB_WORKSPACE', '.')

s = requests.Session()
s.verify = False
token = s.post(f'{API}/access/token',
               data={'username': 'admin', 'password': 'meridian-nifi-2026'}).text
s.headers['Authorization'] = f'Bearer {token}'
root = s.get(f'{API}/flow/process-groups/root').json()['processGroupFlow']['id']


def bundle_of(kind, type_name):
    types = s.get(f'{API}/flow/{kind}-types').json()[f'{kind.replace("-", "")}Types'
                                                    if kind == 'processor' else 'controllerServiceTypes']
    match = [t for t in types if t['type'].endswith('.' + type_name)]
    return match[0]['type'], match[0]['bundle']


def configure(entity_url, entity, settings, extra=None):
    """Set properties by display name; translate displayed choices into their values."""
    comp = entity['component']
    descriptors = comp['config']['descriptors'] if 'config' in comp else comp['descriptors']
    props = {}
    for label, value in settings.items():
        key = [k for k, d in descriptors.items() if d['displayName'] == label]
        if not key:
            sys.exit(f'No property labelled {label!r} on {comp["name"]}: {[d["displayName"] for d in descriptors.values()]}')
        d = descriptors[key[0]]
        for allowed in d.get('allowableValues') or []:
            av = allowed['allowableValue']
            if av['displayName'] == value:
                value = av['value']
        props[key[0]] = value
    body = {'revision': entity['revision'], 'component': {'id': comp['id'], 'properties': props}}
    if 'config' in comp:
        body['component'] = {'id': comp['id'], 'config': {'properties': props, **(extra or {})}}
        if extra and 'name' in extra:
            body['component']['name'] = extra.pop('name')
    r = s.put(entity_url, json=body)
    r.raise_for_status()
    return r.json()


def service(type_name, settings):
    t, b = bundle_of('controller-service', type_name)
    r = s.post(f'{API}/process-groups/{root}/controller-services',
               json={'revision': {'version': 0}, 'component': {'type': t, 'bundle': b}})
    r.raise_for_status()
    e = r.json()
    e = configure(f'{API}/controller-services/{e["id"]}', e, settings)
    r = s.put(f'{API}/controller-services/{e["id"]}/run-status',
              json={'revision': e['revision'], 'state': 'ENABLED'})
    r.raise_for_status()
    return e['id']


def processor(type_name, name, settings, terminate=(), x=0, y=0):
    t, b = bundle_of('processor', type_name)
    r = s.post(f'{API}/process-groups/{root}/processors',
               json={'revision': {'version': 0},
                     'component': {'type': t, 'bundle': b, 'name': name,
                                   'position': {'x': x, 'y': y}}})
    r.raise_for_status()
    e = r.json()
    extra = {'autoTerminatedRelationships': list(terminate)}
    e = configure(f'{API}/processors/{e["id"]}', e, settings, extra)
    return e['id']


def connect(src, dst, relationships):
    r = s.post(f'{API}/process-groups/{root}/connections', json={
        'revision': {'version': 0},
        'component': {'source': {'id': src, 'groupId': root, 'type': 'PROCESSOR'},
                      'destination': {'id': dst, 'groupId': root, 'type': 'PROCESSOR'},
                      'selectedRelationships': relationships}})
    r.raise_for_status()


# Step 4: the two controller services
schema = open(os.path.join(REPO, 'ch03-nifi', 'supplier_stock.avsc')).read()
reader = service('CSVReader', {
    'Schema Access Strategy': "Use 'Schema Text' Property",
    'Schema Text': schema,
    'Treat First Line as Header': 'true',
    'Date Format': 'yyyy-MM-dd',
})
writer = service('JsonRecordSetWriter', {})

# Steps 3 and 5: the processors
get = processor('GetFile', 'GetFile', {
    'Input Directory': '/data/drops', 'File Filter': r'.*\.csv', 'Keep Source File': 'false'})
validate = processor('ValidateRecord', 'ValidateRecord', {
    'Record Reader': reader, 'Record Writer': writer, 'Allow Extra Fields': 'false'}, y=200)
landed = processor('PutFile', 'Write landed', {'Directory': '/data/landed'},
                   terminate=['success'], x=-300, y=400)
quarantine = processor('PutFile', 'Write quarantine', {'Directory': '/data/quarantine'},
                       terminate=['success'], x=300, y=400)

# Step 6: the connections, including the failure loops on the two PutFile boxes
connect(get, validate, ['success'])
connect(validate, landed, ['valid'])
connect(validate, quarantine, ['invalid', 'failure'])
connect(landed, landed, ['failure'])
connect(quarantine, quarantine, ['failure'])

time.sleep(3)
flow = s.get(f'{API}/flow/process-groups/{root}').json()['processGroupFlow']['flow']
problems = {p['component']['name']: p['component'].get('validationErrors')
            for p in flow['processors'] if p['component'].get('validationStatus') != 'VALID'}
print('checkpoint, warning triangles:', problems or 'none')
if problems:
    sys.exit(1)

# Step 7: start everything and drop the file
r = s.put(f'{API}/flow/process-groups/{root}', json={'id': root, 'state': 'RUNNING'})
r.raise_for_status()
shutil.copy(os.path.join(REPO, 'ch02-files-apis-iot', 'supplier_stock.csv'),
            os.path.join(DATA, 'drops'))
for _ in range(30):
    time.sleep(2)
    if glob.glob(f'{DATA}/landed/*') and glob.glob(f'{DATA}/quarantine/*'):
        break
time.sleep(3)

print('drops:', os.listdir(f'{DATA}/drops'))
for folder in ('landed', 'quarantine'):
    files = os.listdir(f'{DATA}/{folder}')
    print(f'{folder}: {files}')
    for f in files:
        text = open(f'{DATA}/{folder}/{f}').read()
        try:
            records = json.loads(text)
            print(f'  {f}: JSON, {len(records)} records')
            if folder == 'quarantine':
                for rec in records:
                    print('   ', rec)
        except json.JSONDecodeError:
            print(f'  {f}: not JSON; first lines:', text.splitlines()[:4])

bulletins = s.get(f'{API}/flow/bulletin-board').json()['bulletinBoard']['bulletins']
for b in bulletins:
    print('bulletin:', b['bulletin'].get('sourceName'), b['bulletin'].get('message', '')[:300])
