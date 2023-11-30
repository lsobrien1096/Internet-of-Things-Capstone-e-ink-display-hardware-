# -------------------------------------------
# ping.py
# Transmits an "I Am Alive" Message
# -------------------------------------------

import sys
import paho.mqtt.client as mqtt
import time
import datetime
import json

# This Gives this Script Access to the Libs Folder
sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm
import systemInfo


# Connects to the MQTT Broker
comm.connect()

# Transmits the Message
comm.send("status", "ping")

# Disconnects from the MQTT Broker
comm.disconnect()









