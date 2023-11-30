import paho.mqtt.client as mqtt
import datetime, time, sys
import json, requests

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm

payload = {}
masterD = {}

# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# Use msg.payload to get the string contents
# ---------------------------------------------
def on_message(client, userdata, msg):   
    # Extracts the Headers (Formatted in JSON)
    message_contents = json.loads(msg.payload)
    
    
    
    # If Message Payload is JSON
    payload = message_contents["payload"]
    try:
        masterD = json.loads(payload)
    except:
        masterD = "Hello"
        print("not json")
    
    if type(masterD) is dict:
        print("Dict")
        if len(masterD.keys())>0:
            print("Sending bluetooth data to website")
            r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data= {'api_key' : '12345','api_function' : 'bluetooth', 'data': json.dumps(masterD)})
            print(r.text)
            print(masterD["BEACON"])
            if masterD["BEACON"] == "874f7565436861726d426561636f6e73":
                print("Unlocking")
                comm.sendLiteral("ring/42d916f2-a6af-480c-a4c0-58ccf6576a49/alarm/332ef73b-d7f8-4099-829b-89ad020547ef/lock/command", "UNLOCK")
            else:
                print("Locking")
                comm.sendLiteral("ring/42d916f2-a6af-480c-a4c0-58ccf6576a49/alarm/332ef73b-d7f8-4099-829b-89ad020547ef/lock/command", "LOCK")

                
    


# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("bluetooth_all", 0)])
# Tells the Listener to Listen Perpetually      
comm.listen(on_message)




