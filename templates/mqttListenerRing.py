import paho.mqtt.client as mqtt
import datetime, time, sys

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm
import json, requests

contact = {}
motion = {}
updateTime = 60

# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# ---------------------------------------------
def on_message(client, userdata, msg):
    print("Custom Message Handler")
    for key in contact:
        if key in msg.topic:
            if "contact/state" in msg.topic:
                if "OFF" in str(msg.payload):
                    print("Sent Off")
                    comm.send("ring", {"room": contact[key], "state": "off"})
                elif "ON" in str(msg.payload):
                    print("Sent On")
                    comm.send("ring", {"room": contact[key], "state": "on"})
    for key in motion:
        if key in msg.topic:
            if "motion/state" in msg.topic:
                if "OFF" in str(msg.payload):
                    print("Sent Off")
                    comm.send("ring", {"room": motion[key], "state": "off"})
                elif "ON" in str(msg.payload):
                    print("Sent On")
                    comm.send("ring", {"room": motion[key], "state": "on"})
            
    
    
    
    


# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
 
comm.connect(channels = [
                         ("ring/42d916f2-a6af-480c-a4c0-58ccf6576a49/alarm/#",0)
                         ]
             )

# Tells the Listener to Listen Perpetually
comm.listen(on_message)

while True:
    url="https://iot.dfcs-cloud.net/ringDevices.php?apiKey=12345"
    response = requests.get(url)
    devices = response.json()
    contact = devices["Contact Sensors"]
    motion = devices["Motion Sensors"]
    time.sleep(updateTime)
    








