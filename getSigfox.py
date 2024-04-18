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
base_topic = url.path[1:] if url.path else "Marine_Monitor_IOT/temp"

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
token = "EoMSb5MEILxDkE1LbiZBPdw_DPuN8BmrF-_0K3ulzvs-Zk7PnEgWq2jBYldbDkN3xI-pkkQK2uJcdgqf2krANA=="
# Define InfluxDB Organisation
org = "your-initial-organisation"
# Define public URL and PORT to InfluxDB 
url = "http://54.90.164.59:8086"
# Define InfluxDB bucket
bucket="your-initial-bucket"


write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

app = Flask(__name__)

# Set HTTP request
@app.route('/sigfox/webhook', methods=['POST'])
def sigfox_webhook():
    data = request.get_json()
    print(data)
    print("received")

    if 'temp' in data:
      # Convert Temp to decimal and from Kelvin to celcius
        temp_value = ((float(data['temp'])/100)-272)
        # MQTT Publish
        mqttc.publish(base_topic + "/temperature", json.dumps({"temperature": temp_value, "timestamp": time.time()}))
        print("Published temperature to MQTT.")

        # InfluxDB POINT
        point = (
            Point("temperature")
            .tag("source", "sigfox")
            .field("value", temp_value)
        )
      # Write to InfluxDB
        write_api.write(bucket=bucket, org=org, record=point)
        print("Data put into DB")
    else:
        print("Temperature data ('temp') not found in the payload")

    return jsonify({'message': 'Data received and processed'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
