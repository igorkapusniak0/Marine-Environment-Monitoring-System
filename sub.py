import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_message(client, obj, msg):
    print("Topic:"+msg.topic + ",Payload:" + str(msg.payload))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed,  QOS granted: "+ str(granted_qos))


mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# parse mqtt url for connection details
url_str = sys.argv[1]
url = urlparse(url_str)
base_topic = url.path[1:]

# Connect
if (url.username):
    mqttc.username_pw_set(url.username, url.password)
try:
    print("Connecting to "+  url_str)    
    mqttc.connect(url.hostname, url.port)
except Exception as e:
    print("Connection failed: " + str(e))
    exit(1)
# Continue the network loop, exit when an error occurs
try:  
    # Start subscribe, with QoS 0
    mqttc.subscribe(base_topic+"/#",qos=0)
    mqttc.loop_forever()
except KeyboardInterrupt:#ctrl+c issues interrupt
    pass
finally:
    mqttc.loop_stop()
    mqttc.disconnect()
    print("Disconnected from MQTT broker.")
