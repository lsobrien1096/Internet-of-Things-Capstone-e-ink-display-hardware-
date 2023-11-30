import paho.mqtt.client as mqtt
import datetime, time, sys

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm
import json
from datetime import datetime
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
        print("Processing Message:", str(message))

        # Processes the Message
        process_message(message)

        print("Processing Complete\n")
        

    except Exception as e:
        print("Problem Processing Message:", str(e), "\n")
        comm.send("ifttt_debug", { "EVENT_NAME": EVENT_NAME, "message":"Error: " + str(e) })
    

initialize()
# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("ring", 0)])
# Tells the Listener to Listen Perpetually
comm.listen(on_message)

def process_message(message_payload):
    global configuration_updated

    # Extracts the Headers (Formatted in JSON)
    message_contents = json.loads(message_payload)
    
    # Checks to See if the Payload is Already a Dictionary
    # or a String that Needs to be Processed as a Dictionary
    if type(message_contents["payload"]) is dict:
        data = message_contents["payload"]
    else:
        data = json.loads(message_contents["payload"])
        
    print(data)
    payload_arr = []
    payload_arr_tts = []
    ttsPayload = ""
    
    time = datetime.now()
    currentTime = time.hour
    print(currentTime)
    #currentTime = 13
    
    if (data["room"] == "ACCR Backdoor" and data["state"] == "on") and (currentTime >= 9 and currentTime <= 12):
        payload = {}
        payload['array'] = 1
        payload['light'] = 3
        payload['r'] = 0
        payload['g'] = 255
        payload['b'] = 0
        payload_arr.append(payload)

    if (data["room"] == "ACCR Backdoor" and data["state"] == "off") and (currentTime >= 9 and currentTime <= 12):
        payload = {}
        payload['array'] = 1
        payload['light'] = 3
        payload['r'] = 255
        payload['g'] = 0
        payload['b'] = 0
        payload_arr.append(payload)
#         
#     if (data["room"] == "ACCR Backdoor" and data["state"] == "on") and (currentTime <= 9 or currentTime >= 12):
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 3
#         payload['r'] = 255
#         payload['g'] = 255
#         payload['b'] = 0
#         payload_arr.append(payload)
#         
#     if (data["room"] == "ACCR Backdoor" and data["state"] == "off") and (currentTime <= 9 or currentTime >= 12):
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 3
#         payload['r'] = 0
#         payload['g'] = 100
#         payload['b'] = 255
#         payload_arr.append(payload)
#     
#     if data["room"] == "ACCR Backdoor" and data["state"] == "on":
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 3
#         payload['r'] = 0
#         payload['g'] = 255
#         payload['b'] = 0
#         payload_arr.append(payload)
#     if data["room"] == "ACCR Backdoor" and data["state"] == "off":
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 3
#         payload['r'] = 255
#         payload['g'] = 0
#         payload['b'] = 0
#         payload_arr.append(payload)
#     
    #Controls light in DFCS
#     if data["room"] == "ACCR Backdoor" and data["state"] == "on":
#         payload = {}
#         payload['array'] = 6
#         payload['light'] = "*"
#         payload['r'] = 255
#         payload['g'] = 0
#         payload['b'] = 0
#         payload_arr.append(payload)
#     if data["room"] == "ACCR Backdoor" and data["state"] == "off":
#         payload = {}
#         payload['array'] = 6
#         payload['light'] = "*"
#         payload['r'] = 0
#         payload['g'] = 255
#         payload['b'] = 0
#         payload_arr.append(payload)
#      
#     if data["room"] == "Cyber City Door" and data["state"] == "on":
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 2
#         payload['r'] = 0
#         payload['g'] = 255
#         payload['b'] = 0
#         payload_arr.append(payload)
#     if data["room"] == "Cyber City Door" and data["state"] == "off":
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 2
#         payload['r'] = 255
#         payload['g'] = 0
#         payload['b'] = 0
#         payload_arr.append(payload)
#         
#     if data["room"] == "Cyber City Motion" and data["state"] == "on":
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 4
#         payload['r'] = 0
#         payload['g'] = 255
#         payload['b'] = 0
#         payload_arr.append(payload)
#     if data["room"] == "Cyber City Motion" and data["state"] == "off":
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 4
#         payload['r'] = 255
#         payload['g'] = 0
#         payload['b'] = 0
#         payload_arr.append(payload)
#         
#     if data["room"] == "ACCR Frontdoor" and data["state"] == "on":
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 1
#         payload['r'] = 0
#         payload['g'] = 255
#         payload['b'] = 0
#         payload_arr.append(payload)
#     if data["room"] == "ACCR Frontdoor" and data["state"] == "off":
#         payload = {}
#         payload['array'] = 1
#         payload['light'] = 1
#         payload['r'] = 255
#         payload['g'] = 0
#         payload['b'] = 0
#         payload_arr.append(payload)
#     
#     if data["room"] == "ACCR Backdoor" and data["state"] == "on":
#         ttspayload = "meow"
#         payload_arr_tts.append(ttspayload)
#     if data["room"] == "ACCR Backdoor" and data["state"] == "off":
#         ttspayload = "meow"
#         payload_arr_tts.append(ttspayload)
#         
#     if data["room"] == "Cyber City Door" and data["state"] == "on":
#         ttspayload = "Cyber City Door Open"
#         payload_arr_tts.append(ttspayload)
#     if data["room"] == "Cyber City Door" and data["state"] == "off":
#         ttspayload = "Cyber City Door Closed"
#         payload_arr_tts.append(ttspayload)
#         
#     if data["room"] == "Cyber City Motion" and data["state"] == "on":
#         ttspayload = "Cyber City Motion Detected"
#         payload_arr_tts.append(ttspayload)
#         
#     if data["room"] == "ACCR Frontdoor" and data["state"] == "on":
#         ttspayload = "A.C.C.R Frontdoor Open"
#         payload_arr_tts.append(ttspayload)
#     if data["room"] == "ACCR Frontdoor" and data["state"] == "off":
#         ttspayload = "A.C.C.R Frontdoor Closed"
#         payload_arr_tts.append(ttspayload)
#     print("HERE")
    print(payload_arr)
    for x in payload_arr:
        print(x)
        comm.send("lights", x)
    payload_arr.clear()
#    print("NOWHERE")
#    for x in payload_arr_tts:
#       comm.send("tts", x)   
#    payload_arr_tts.clear()
    
    


    










