"""Exercise 5 — alert when the cold room rises above 6.0 °C."""
import json

import paho.mqtt.client as mqtt

LIMIT_C = 6.0


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe('meridian/warehouse/cold-room')


def on_message(client, userdata, msg):
    r = json.loads(msg.payload)
    if r['temp_c'] > LIMIT_C:
        print(f"ALERT cold-room seq={r['seq']} "
              f"temp={r['temp_c']} at {r['ts']}")
        client.disconnect()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='cold-room-alert')
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883)
client.loop_forever()
