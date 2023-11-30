import paho.mqtt.client as mqtt
import datetime, time, sys
import json

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
    
    # If Message Payload is JSON
    # payload = json.loads(message_contents["payload"])


# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("status", 0),
                         ("bluetooth_all", 0),
                         ("image_classify", 0)]
             )

# Tells the Listener to Listen Perpetually
comm.listen(on_message)



