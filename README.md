# Marine-Environment-Monitoring-System
For this project we aim to develop a marine environment monitoring system to gather critical data on the temperature of water, wave dynamics and PH levels.

Our approach involves utilising a variety of sensors, including a thermistor or waterproof thermometer for temperature measurements, a gyroscope to capture wave data, and a pH sensor for water acidity. These sensors will be integrated with an Arduino Nano, which will serve for the processing of data. The data collected will then be transmitted via a Sigfox microcontroller to the Sigfox cloud.

To allow for proper functioning in a marine setting, the microcontrollers and sensors would be powered by a battery within the range of 5-9 volts. This setup will be encased in a transparent and waterproof container, anchored at the base to maintain stability and ensure accurate gyroscope readings. 

Once the data reaches the Sigfox cloud it will be sent through a MQTT broker to a MongoDB database located on an AWS EC2 instance or a local server. This database implementation is crucial for enabling long term access to the data.

For visualisation and interaction of the collected data, platforms such as Blynk or ThingSpeak will be used, as they offer an easy way for displaying data through graphs and other methods. 

# Tools, Technology and Equipment
Software:
Python, C++, MongoDB, ThingSpeak/Blynk
Hardware:
Arduino Nano, Sigfox Microcontroller and antenna, thermistor or waterproof thermometer, gyroscope sensor, wires, waterproof container, rubber seals, 
5v-9v battery (solar panel if possible), weight.

