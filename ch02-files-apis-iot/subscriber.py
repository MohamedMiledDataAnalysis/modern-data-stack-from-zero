"""Chapter 2, Step 6 — receive warehouse sensor readings over MQTT."""
import json

import paho.mqtt.client as mqtt

MAX_MESSAGES = 9
received = []


def on_connect(client, userdata, flags, reason_code, properties):
    print('Connected:', reason_code)
    client.subscribe('meridian/warehouse/#')


def on_message(client, userdata, msg):
    reading = json.loads(msg.payload)
    received.append(reading)
    print(f"{msg.topic:<32} seq={reading['seq']} "
          f"temp={reading['temp_c']}")
    if len(received) == MAX_MESSAGES:
        client.disconnect()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='meridian-reader')
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883)
client.loop_forever()
print(f'{len(received)} readings received')
