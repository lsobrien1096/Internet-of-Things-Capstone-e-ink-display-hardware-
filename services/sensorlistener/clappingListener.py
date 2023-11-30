import paho.mqtt.client as mqtt
import time, sys
import json
from datetime import datetime

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm


# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# Use msg.payload to get the string contents
# ---------------------------------------------
def on_message(client, userdata, msg):
    print("Custom Message Handler")
    
    # Extracts the Headers (Formatted in JSON)
    message_contents = json.loads(msg.payload)
    dt = datetime.now()
    
    # If Message Payload is JSON
    payload = json.loads(message_contents["payload"])
    payload_arr = []
    if payload["Class"] == "2 Knocking":
        
        print("Unlocking")
        comm.sendLiteral("ring/42d916f2-a6af-480c-a4c0-58ccf6576a49/alarm/332ef73b-d7f8-4099-829b-89ad020547ef/lock/command", "UNLOCK")   
    else:
        
        print("Locking")
        comm.sendLiteral("ring/42d916f2-a6af-480c-a4c0-58ccf6576a49/alarm/332ef73b-d7f8-4099-829b-89ad020547ef/lock/command", "LOCK")


# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("knocks", 0)]
             )

# Tells the Listener to Listen Perpetually
comm.listen(on_message)



