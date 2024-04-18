# Marine-Environment-Monitoring-System

For this project we aim to develop a marine environment monitoring system to gather data on the temperature of water.

Our approach involves utilising a variety of sensors, including a waterproof thermometer for temperature measurements. The sensor will be integrated with an Arduino Nano, which will serve for the processing of data. The data collected will then be transmitted via a Pycom SiPy microcontroller to the Sigfox cloud.

To allow for proper functioning in a marine setting, the microcontrollers and sensors would be powered by a battery of 4.5 volts. This setup will be encased in a transparent and waterproof container, anchored at the base to maintain stability. 

Once the data reaches the Sigfox cloud it will be sent to ThingSpeak and an AWS EC2 instance where the data is sent to a MQTT broker for public access and to a Influx database located on the instance. This database implementation is crucial for enabling long term access to the data.

For visualisation and interaction of the collected data, ThingSpeak will be used, as they offer an easy way for displaying data through graphs and other methods. 

# Tools, Technology and Equipment
Software:
Python, C++, InfluxDB, ThingSpeak, Sigfox, Docker, Solidworks, Cura Slicer, MQTT
Hardware:
Arduino Nano, Sigfox Microcontroller and antenna, thermistor or waterproof thermometer, gyroscope sensor, wires, waterproof container, rubber seals, 3x1.5V battery, weight.

# Set Up

Install dependencies:
```bash
pip3 install -r requirements.txt
sudo apt install docker
sudo apt-get install mosquitto
```

Setting Up InfluxDB
Pull the container
```
docker pull influxdb
```
Next, set the relevant information for the container.\
For more information visit: https://hub.docker.com/_/influxdb
```
docker run -d -p 8086:8086 \
  -v "$PWD/data:/var/lib/influxdb2" \
  -v "$PWD/config:/etc/influxdb2" \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=<USERNAME> \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=<PASSWORD> \
  -e DOCKER_INFLUXDB_INIT_ORG=<ORG_NAME> \
  -e DOCKER_INFLUXDB_INIT_BUCKET=<BUCKET_NAME> \
  influxdb:2
```

