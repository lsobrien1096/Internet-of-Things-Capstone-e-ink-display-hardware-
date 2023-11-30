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
    print("Custom Message Handler abcd")
    for key in contact:
        if key in msg.topic:
            print("TOPIC:", msg.topic)
            if "contact/state" in msg.topic:
                if "OFF" in str(msg.payload):
                    print("Sent Off")
                    comm.send("ring", {"room": contact[key], "state": "off"})
                    d = {
                            "device_id": key,
                            "device_type": "contact",
                            "device_room": contact[key],
                            "device_state":"off"
                        }
                    print("Starting HTTP")
                    r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data= {'api_key' : '12345','api_function' : 'ring', 'data': json.dumps(d)})
                    print("ENDING HTTP: ", r.text)
                elif "ON" in str(msg.payload):
                    print("Sent On")
                    comm.send("ring", {"room": contact[key], "state": "on"})
                    d = {
            
                            "device_id": key,
                            "device_type": "contact",
                            "device_room": contact[key],
                            "device_state":"on"
                        }
                    print("Starting HTTP")
                    r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data= {'api_key' : '12345','api_function' : 'ring', 'data': json.dumps(d)})
                    print("ENDING HTTP: ",r.text)
    for key in motion:
        if key in msg.topic:
            if "motion/state" in msg.topic:
                if "OFF" in str(msg.payload):
                    print("Sent Off")
                    comm.send("ring", {"room": motion[key], "state": "off"})
                    d = {
            
                            "device_id": key,
                            "device_type": "motion",
                            "device_room": motion[key],
                            "device_state":"off"
                        }
                    r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data= {'api_key' : '12345','api_function' : 'ring', 'data': json.dumps(d)})
                    print(r.text)
                elif "ON" in str(msg.payload):
                    print("Sent On")
                    comm.send("ring", {"room": motion[key], "state": "on"})
                    d = {
            
                            "device_id": key,
                            "device_type": "motion",
                            "device_room": motion[key],
                            "device_state":"on"
                        }
                    r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data= {'api_key' : '12345','api_function' : 'ring', 'data': json.dumps(d)})
                    print(r.text)
            
    
    
    
    


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
    








