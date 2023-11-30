import requests, time, math, json
import paho.mqtt.client as mqtt
import datetime, time, sys
sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm
import pywemo

DEVICE_NUM = 0
COMMAND = ""
ID = ""

#discovers all Wemo devices on the network
devices = pywemo.discover_devices()
print(devices)
printableDevices = []
for x in devices:
    myString = str(x)
    printableDevices.append(myString)
def initialize():
    global DEVICE_NUM, COMMAND

def on_message(client, userdata, message):
    message = message.payload
           

    try:
        print("Processing Message:", str(message))

        # Processes the Message
        process_message(message)

        print("Processing Complete\n")

    except Exception as e:
        print("Problem Processing Message:", str(e), "\n")
        comm.send("wemo_debug", { "deviceNum":DEVICE_NUM, "message":"Error: " + str(e) })

initialize()
# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("wemo", 0)])
# Tells the Listener to Listen Perpetually
comm.listen(on_message)
 
#payload = {deviceNum, command}
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
        
    #sends commands to Wemo device
    COMMAND = data['command']
    print(COMMAND)
    deviceNum = 0
    for x in printableDevices:
        if data['id'] in x:
            print(str(devices[deviceNum]) + "Has been found in the array")
            if COMMAND == "on":
                print(str(devices[deviceNum]) + "Has been turned on")
                devices[deviceNum].on()
            elif COMMAND == "off":
                print(str(devices[deviceNum]) + "Has been turned off")
                devices[deviceNum].off()
            else:
                print(str(devices[deviceNum]) + "Has been toggled")
                devices[deviceNum].toggle()
        deviceNum = deviceNum + 1

    
    
