"""Chapter 2 — simulate Meridian warehouse sensors publishing over MQTT.

Publishes one reading per sensor every second to meridian/warehouse/<zone>.
Stop it with Ctrl+C. Seed 3 gives every reader the same readings.
"""
import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

random.seed(3)
ZONES = ['cold-room', 'dry-store', 'loading-bay']

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='sensor-sim')
client.connect('localhost', 1883)
client.loop_start()

n = 0
try:
    while True:
        for zone in ZONES:
            base = 4.0 if zone == 'cold-room' else 18.0
            reading = {'zone': zone, 'seq': n,
                       'temp_c': round(base + random.gauss(0, 1.5), 1),
                       'humidity': random.randint(35, 60),
                       'ts': datetime.now(timezone.utc).isoformat(timespec='seconds')}
            client.publish(f'meridian/warehouse/{zone}', json.dumps(reading))
        n += 1
        time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
