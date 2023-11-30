'''
To create an applet to work with this code, when selecting the trigger event, select the Webhooks service. Once selected,
select the "receive a web request" trigger. 
'''
import paho.mqtt.client as mqtt
import datetime, time, sys

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm
import json
from pathlib import Path
import requests

EVENT_NAME = None
configuration_updated = True  

# ----------------------------------------------
# Sets Up Variables/Settings Prior to Listening
# ----------------------------------------------
def initialize():
    global EVENT_NAME, URL, value1, state
# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# ---------------------------------------------
def on_message(client, userdata, message):
    message = message.payload        

    try:
        print("Processing Message:", message)

        # Processes the Message
        process_message(message)

        print("Processing Complete\n")

    except Exception as e:
        print("Problem Processing Message:", str(e), "\n")
        comm.send("ifttt_debug", { "EVENT_NAME": EVENT_NAME, "message":"Error: " + str(e) })
    

initialize()
# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("camera", 0)])
# Tells the Listener to Listen Perpetually
comm.listen(on_message)

def process_message(message_payload):
    global configuration_updated

    # Extracts the Headers (Formatted in JSON)
    message_contents = message_payload.decode()
    bigdata = json.loads(message_contents)
    for entry in bigdata['payload']:
        data = entry
        
    print(data)
    payload_arr = []
    
    if data["class"] == "Full" and data["score"] >= 0.8:
        payload = {}
        payload['array'] = 1
        payload['light'] = "5"
        payload['r'] = 255
        payload['g'] = 0
        payload['b'] = 0
        payload_arr.append(payload)
    if data["class"] == "Available" and data["score"] >= 0.6:
        payload = {}
        payload['array'] = 1
        payload['light'] = "5"
        payload['r'] = 0
        payload['g'] = 255
        payload['b'] = 0
        payload_arr.append(payload)
    
   
    
    for x in payload_arr:
        comm.send("lights", x)
    payload_arr.clear()
    


    











