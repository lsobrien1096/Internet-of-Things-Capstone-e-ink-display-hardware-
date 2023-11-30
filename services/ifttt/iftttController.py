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

# THIS IS THE KEY PROVIDED BY IFTTT
IFTTT_KEY = "jh7iaXuQuGQv8sCwkup34iIpelbjAMzQZZxB5Yt9_K2"


# ----------------------------------------------
# Sets Up Variables/Settings Prior to Listening
# ----------------------------------------------
def initialize():
    pass


# ---------------------------------------------
# Creates a URL to Control the IFTTT Event
# ---------------------------------------------
def getURL(ifttt_event):
    return "https://maker.ifttt.com/trigger/" + str(ifttt_event) + "/with/key/" + IFTTT_KEY


# ---------------------------------------------
#
# ---------------------------------------------
def process_message(message_payload):
    global configuration_updated

    # Extracts the Headers (Formatted in JSON)
    message_contents = json.loads(message_payload)
    
    # Checks to See if the Payload is Already a Dictionary
    # or a String that Needs to be Processed as a Dictionary
    if type(message_contents["payload"]) is dict:
        print("Processing as dictionary")
        data = message_contents["payload"]
    else:
        print("Processing as string")
        data = json.loads(message_contents["payload"])

    if 'EVENT_NAME' in data:
        print("Triggering IFTTT Event:", data['EVENT_NAME'])
        response = requests.get(getURL(data['EVENT_NAME']))
        print("IFTTT Response:", response.text)
    else:
        print("Could not find EVENT_NAME", data)


# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# ---------------------------------------------
def on_message(client, userdata, message):
    message = message.payload        

    try:
        print("Processing Message:", str(message))

        # Processes the Message
        process_message(message)

        print("Processing Complete\n")

    except Exception as e:
        print("Problem Processing Message:", str(e), "\n")
        comm.send("ifttt_debug", { "EVENT_NAME":EVENT_NAME, "message":"Error: " + str(e) })
    

initialize()

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("ifttt", 0)])

# Tells the Listener to Listen Perpetually
comm.listen(on_message)






