import paho.mqtt.client as mqtt
import datetime, time, sys
import json, requests
import time

sys.path.append("/home/usafaiot/Desktop/iotcapstone/libs")
import comm


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
            
            "hostname":message_contents['hostname'],
            "network":message_contents['network'],
            "ip":message_contents['ip'],
            "timestamp":message_contents['timestamp'],
            "payload":message_contents['payload']
        }
    
    masterD[message_contents['hostname']]=  d
        
    

        
        

        
    # If Message Payload is JSON
    # payload = json.loads(message_contents["payload"]) 

# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("status", 0)])

# Tells the Listener to Listen Perpetually
comm.listen(on_message)

#Pauses the program for 1 minute then repeats indefinitely 
while True:
    if len(masterD.keys())>0:
        r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data= {'api_key' : '12345', 'data': json.dumps(masterD)})
        print("hi:", r.text)
        #print(masterD)
        masterD={}



