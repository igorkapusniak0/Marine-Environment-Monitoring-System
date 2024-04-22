import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
import time
import json
from flask import Flask, request, jsonify
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

mqttc = mqtt.Client()

# Define event callbacks for MQTT
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    print("Message ID: " + str(mid))

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# Define MQTT Broker
url_str = "mqtt://broker.emqx.io:1883"
url = urlparse(url_str)
# Define MQTT Topic
base_topic = url.path[1:] if url.path else "Your/Topic"

# Connect to MQTT
if url.username:
    mqttc.username_pw_set(url.username, url.password)
try:
    print("Connecting to "+ url_str)
    mqttc.connect(url.hostname, url.port)
    mqttc.loop_start()
except Exception as e:
    print("Connection failed: " + str(e))
    sys.exit(1)



# Define InfluxDB Token
INFLUXDB_TOKEN = "INFLUXDB-API-TOCKEN"
# Define InfluxDB Organisation
INFLUXDB_ORGANISATION = "your-initial-organisation"
# Define public URL and PORT to InfluxDB 
INFLUXDB_URL = "http://Your IP Address:8086"
# Define InfluxDB bucket
INFLUXDB_BUCKET="your-initial-bucket"


write_client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORGANISATION)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

app = Flask(__name__)

# Set HTTP request
@app.route('/sigfox/webhook', methods=['POST'])
def sigfox_webhook():
    data = request.get_json()
    print(data)
    print("received")

    if data:
        for key, value in data.items():
            if isinstance(value, (int, float)):  # Check if the value is numeric
                # Convert temperature from Kelvin to Celsius if key is 'temp'
                if key == 'temp':
                    value = (value / 100) - 273
                
                # MQTT Publish
                mqtt_topic = f"{base_topic}/{key}"
                mqttc.publish(mqtt_topic, json.dumps({key: value, "timestamp": time.time()}))
                print(f"Published {key} to MQTT: {value}")

                # InfluxDB Point
                point = (
                    Point("sensor_data")
                    .tag("source", "sigfox")
                    .tag("sensor_type", key)  # Tag each point with the key
                    .field("value", value)
                )
                # Write to InfluxDB
                write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORGANISATION, record=point)
                print(f"Data written to DB for {key}")
            else:
                print(f"Skipping {key}, not a numeric value")
    else:
        print("No data found in the payload")

    return jsonify({'message': 'Data received and processed'})

if __name__ == '__main__':
    # Change port if port is already taken
    app.run(debug=True, host='0.0.0.0', port='5000')
