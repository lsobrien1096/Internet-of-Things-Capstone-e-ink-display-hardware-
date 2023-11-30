import requests, time, math, json
import paho.mqtt.client as mqtt
import datetime, time, sys
sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm
import pywemo

devices = pywemo.discover_devices()
print(devices)
comm.connect()

#can be on, off, toggle
COMMAND = "null"
ID = "null"
while (COMMAND != "exit"):
    ID = input("Device Name: ")
    COMMAND = input("Command: ")

    payload = {}
    payload["command"] = COMMAND
    payload["id"] = ID

    comm.send("wemo", payload)





