# Marine-Environment-Monitoring-System

## Overview
This project develops a marine environment monitoring system to gather data on water temperature. Utilizing a combination of sensors and microcontrollers, the system captures real-time temperature data, transmitting it securely to the cloud for analysis and public access. 

For this project we aim to develop a marine environment monitoring system to gather data on the temperature of water.

Our approach involves utilising a variety of sensors, including a waterproof thermometer for temperature measurements. The sensor will be integrated with an Arduino Nano, which will serve for the processing of data. The data collected will then be transmitted via a Pycom SiPy microcontroller to the Sigfox cloud.

To allow for proper functioning in a marine setting, the microcontrollers and sensors would be powered by a battery of 4.5 volts. This setup will be encased in a transparent and waterproof container, anchored at the base to maintain stability. 

Once the data reaches the Sigfox cloud it will be sent to ThingSpeak and an AWS EC2 instance where the data is sent to a MQTT broker for public access and to a Influx database located on the instance. This database implementation is crucial for enabling long term access to the data.

For visualisation and interaction of the collected data, ThingSpeak will be used, as they offer an easy way for displaying data through graphs and other methods. 

## Prerequisites
- Basic knowledge of electronics and programming
- Familiarity with Python, C++, and IoT concepts
- Operating System: Linux
- Familiarity with 3D printing, modeling and slicing

## Tools, Technology, and Equipment
### Software
- Python, C++, InfluxDB, ThingSpeak, Sigfox, Docker, MQTT, Solidworks, Cura

### Hardware
- Arduino Nano
- Pycom SiPy Microcontroller and antenna
- DS18B20 - Waterproof Thermometer
- Wires, waterproof container, rubber seals, 3x1.5V battery, weight

# Software Set Up

## Installation

First, install the necessary software dependencies:
```bash
pip3 install -r requirements.txt
sudo apt install docker
sudo apt-get install mosquitto
```

### Setting Up InfluxDB
Pull the container
```bash
docker pull influxdb
```
Configure and run the InfluxDB container:\

```bash
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
For more information visit: https://hub.docker.com/_/influxdb

### Setting up getSigfox.py
This script with recieve data from the [Sigfox Backend](https://backend.sigfox.com/) and send it the database and the MQTT Broker


#### Obtaining InfluxDB tocken
First get the InfluxDB tocken by going to the the servers ip address with the correct port number. \
Login using username and password set before \
Once on the main page select the box with the Python logo \
![image](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/assets/114166214/fdff44be-a8cb-4327-a146-fea786886619) 

This will bring you to this page: \ 
![image](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/assets/114166214/f8c04c02-74d5-4461-a9e0-02fe63e937af) 

From there click on 3rd Circle labeled Get Token:

![image](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/assets/114166214/33b7b528-5c52-43ca-87de-d7a0f70820b5)

Copy it and save it!


### Initial Configuration
Before setting up the service, you need to configure the `getSigfox.py` script with your specific database and MQTT broker settings. \

1. Open the script in an editor:
```bash
   sudo nano /home/ubuntu/path/to/your/script/getSigfox.py
```
Modify the following variables with your details:
- url_str: Your MQTT Broker URL
- base_topic: Your MQTT Topic
- INFLUXDB_TOKEN: Your InfluxDB Token
- INFLUXDB_ORGANISATION: Your InfluxDB organisation
- INFLUXDB_URL: Your URL to the Server and Port to InfluxDB
- INFLUXDB_BUCKET: Your InfluxDB Bucket

- Save the changes and exit the editor.

```bash
sudo nano /etc/systemd/system/getSigfox.service
```
In the editor, add the following configuration: \
Make sure to adjust the Working and ExecStart Directory to your own
```bash
[Unit]
Description=My Python Script Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/path/to/your/script
ExecStart=/usr/bin/python3 /home/ubuntu/path/to/your/script/getSigfox.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Reload Systemd: This updates systemd to recognize your new service.
```bash
sudo systemctl daemon-reload
```
Enable the Service: This sets your script to start at boot.
```bash
sudo systemctl enable myscript.service
```
Start the Service: To start running your service immediately.
```bash
sudo systemctl start myscript.service
```
Check the Status: To verify that your service is active and running.
```bash
sudo systemctl status myscript.service
```

# Hardware Setup

### Equipment:
Arduino Nano \
Pycom SiPy \
DS18B20 - Waterproof Thermometer 

### Arduino wiring Diagram:

![image](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/assets/114166214/d48e4518-a2b0-4354-925b-933105d0f2d6)

### Pycom SiPy Datasheet: 

Arduino Tx goes to P16 \
Battery pack connects to Vin and GND

![image](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/assets/114166214/7819c774-5575-4627-8ca1-bcad84961384)


## Sigfox to Influx
To connect the Sigfox backend to the Influxdb set up the callback as seen below
![image](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/assets/114166214/1d170561-0f2b-4da3-99f8-2866ba5c6515)

## Sigfox to ThingSpeak
To connect the Sigfox backend to Thingspeak set up the callback as seen below
![image](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/assets/114166214/3a6949dd-3de5-4ada-843e-efbaead97604)

## MQTT Subscribe:
To access the data from the MQTT broker run the following commamd \
Your/Topic needs to be replaced with the same one as set in getSigfox.py
```bash
python3 sub.py mqtt://broker.emqx.io:1883/Your/Topic
```

## 3d Printing and Assembly
A few components need to be printed multiple times: \
28 x ([Nut](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/blob/c814bcd994393994a3dece5189b4657378aa8260/Solidworks%20File/nut_6x9.SLDPRT)) \
4 x ([Threaded Bar](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/blob/04f4654d1790fb3020a880b02dd85652b2ad62f4/STL%20Files/threaded_rod_8x100.stl))

All other files need to be printed once


A fully assembled holder should look like this: ([Full Assembly](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/blob/main/Full%20Assembly.STL))


## Configuation of additional sensors
To expand this project to work with additional sensors, a few changes need to be made.

1. Sensor need to be soldered correctly to aduino.
2. Correct libraries need to be imported.
3. Data collected needs to be printed to serial.
4. (Optional) if sensor needs room another disk should be 3D printed.
5. Set up a channel on Thingspeak for recieving new data.
6. Set up callbacks from the Sigfox Backend to Thingspeak and InfluxDB (give it an appropriate key that differs from 'temp') 
   The Python script should not need to change (unless the data needs to be modified in some way) as the data is inserted dynamically based on the key specified in the callback.


## Gif of End Product
![ezgif-3-d903da6700](https://github.com/igorkapusniak0/Marine-Environment-Monitoring-System/assets/114166214/dd8b5079-44b3-40b0-9fb1-27d69c10081b)





