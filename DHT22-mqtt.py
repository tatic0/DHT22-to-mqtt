#!/usr/bin/python

## This script is based on the examples provided by Adafruit.
## See README for Copyright information

import subprocess
import re
import sys
import time
import datetime
import Adafruit_BMP.BMP085 as BMP085
import paho.mqtt.client as paho

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
# How long to wait (in seconds) between measurements.
client = paho.Client()
client.on_connect = on_connect
client.connect("mqtt.broker.your", 1883)
client.loop_start()

freq = 600  # refresh 10 min



try:
# Continuously append data
  while True:
    output = subprocess.check_output(["./Adafruit_DHT", "22", "4"]); ### DEBUG
    print(output)
    # search for temperature printout
    matches = re.search("Temp =\s+([0-9.]+)", output.decode('utf-8'))
    if (not matches):
      time.sleep(3)
      continue
    temp = str(float(matches.group(1)))
    
    # search for humidity printout
    matches = re.search("Hum =\s+([0-9.]+)", output.decode('utf-8'))
    if (not matches):
      time.sleep(3)
      continue
    humidity = str(float(matches.group(1)))
    
    now = str(time.time())
    print(now,temp,humidity)
    # Wait half an hour between each measurement
    (rc, mid) = client.publish("sensor/temp", temp, qos=1)
    (rc, mid) = client.publish("sensor/humidity", humidity, qos=1)
    time.sleep(freq)
except KeyboardInterrupt:
  print("You pressed ctrl-c, quitting")
  sys.exit(0)
