import paho.mqtt.client as mqtt
import datetime, time, sys
import json, requests
import time

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm


# TODO
# Create a way to store all of the status messages from the pis
# Write a loop that, every minute, sends the messages (you stored above) to a URL that taylor gives you
# after you send it, clear the history, and repeat
updateTime = 60
masterD= {}
postRequest = {}

# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# Use msg.payload to get the string contents
# ---------------------------------------------
def on_message(client, userdata, msg):
    print("Custom Message Handler")
    
    # Extracts the Headers (Formatted in JSON)
    message_contents = json.loads(msg.payload)
    
    
    d = {
            "timestamp":message_contents['timestamp'],
            "payload":message_contents['payload']
        }
    
    r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data= {'api_key' : '12345', 'api_function' : 'ring', 'data': json.dumps(d)})
    print(r)
    

        
        

        
    # If Message Payload is JSON
    # payload = json.loads(message_contents["payload"]) 

# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("ring", 0)])

# Tells the Listener to Listen Perpetually
comm.listen(on_message)

#Pauses the program for 1 minute then repeats indefinitely 




