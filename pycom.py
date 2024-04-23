from machine import UART
import os
from network import Sigfox
import socket
import ubinascii
import time
import pycom

uart = UART(1, baudrate=9600)
uart.init(9600, bits=8, parity=None, stop=2, pins=('G17', 'G16'))

sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
pycom.heartbeat(False)

while True:
    if uart.any():
        received_data = uart.read()
        #time.sleep(15)
        if received_data:
            try:
                message = received_data.decode('utf-8').strip()
                print("Received:", message)
                
                temp_float = float(message) + 273
                temp_int = int(temp_float * 100)
                print(temp_int)
                
                temp_bytes = temp_int.to_bytes(2, 'big')
                print(temp_bytes)
                
                s.send(temp_bytes)
                print("sent")
                
            except UnicodeError:
                print("Received data that could not be decoded as UTF-8.")
            except ValueError:
                print("Received data that could not be converted to a floating-point number.")
