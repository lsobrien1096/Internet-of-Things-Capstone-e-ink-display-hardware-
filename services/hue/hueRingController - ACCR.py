import requests, time, math, json
# url = 'http://192.168.1.205/api/newdeveloper'
# 
# x = requests.get(url)


import paho.mqtt.client as mqtt
import datetime, time, sys

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm

LIGHT_ARRAY = None
HUE_IP = None
HUE_APIKEY = None
LIGHT_DELAY = 1.0
lights = []
light_configuration = {}
configuration_updated = True  
maxb = 254
midb = 127



# ----------------------------------------------
# Sets Up Variables/Settings Prior to Listening
# ----------------------------------------------
def initialize():
    global LIGHT_ARRAY, HUE_IP, HUE_APIKEY, lights
    HUE_IP = '192.168.1.205'
    HUE_APIKEY = 'Zg6oDxP313px-XvfT4wpa6tE44d5Nc22DonjMpfp'
    
# ----------------------------------------------
# Used in the RGB converter to make the Hue controller work. 
# ----------------------------------------------
def EnhanceColor(normalized):
    if normalized > 0.04045:
        return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92

# ----------------------------------------------
# Basic RGB converter that allows Hues to work with MQTT
# ----------------------------------------------
def RGBtoXY(r, g, b):
    rNorm = r / 255.0
    gNorm = g / 255.0
    bNorm = b / 255.0

    rFinal = EnhanceColor(rNorm)
    gFinal = EnhanceZg6oDxP313px-XvfT4wpa6tE44d5Nc22DonjMpfpColor(gNorm)
    bFinal = EnhanceColor(bNorm)
    
    X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
    Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
    Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

    if X + Y + Z == 0:
        return (0,0)
    else:
        xFinal = X / (X + Y + Z)
        yFinal = Y / (X + Y + Z)
    
        return (xFinal, yFinal)
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
        comm.send("hue_debug", { "array":LIGHT_ARRAY, "message":"Error: " + str(e) })
   
#EX API KEY Zg6oDxP313px-XvfT4wpa6tE44d5Nc22DonjMpfp
# ----------------------------------------------
# This is the main function that posts a color change to the Hue
# using the Hue API that is posted in the .md file.
# ----------------------------------------------
def update_lights(r, g, b):
    if (r == 0 and g == 0 and b == 0):
        color = RGBtoXY(r, g, b)
        for i in range(1, 100):
            url = 'http://' + str(HUE_IP) + '/api/' + str(HUE_APIKEY) + '/lights/' + str(i) + '/state'
            data = {"on":False, "bri": midb, "xy": [color[0], color[1]]}
            x = requests.put(url, json=data)
    else:    
        color = RGBtoXY(r, g, b)
        for i in range(1, 100):
            url = 'http://' + str(HUE_IP) + '/api/' + str(HUE_APIKEY) + '/lights/' + str(i) + '/state'
            data = {"on":True, "bri": midb, "xy": [color[0], color[1]]}
            x = requests.put(url, json=data) 

# --------------------------------------------
# Main Program
# --------------------------------------------

initialize()
# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("lights", 0)])

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
    
    # Attempts to Configure Lights Set for this Array
    if data['array'] == LIGHT_ARRAY or data['array'] == "*":
        print("Processing command")
        r = int(data['r'])
        g = int(data['g'])
        b = int(data['b'])
        color = RGBtoXY(r, g, b)
        #update_lights(r, g, b)

        if data['light'] != '*':
            # Controlling an Individual Light
            i = int(data['light'])
            print("Light", i, "color changed to", (r, g, b))
            url = 'http://' + str(HUE_IP) + '/api/' + str(HUE_APIKEY) +'/lights/' + str(i) + '/state'
            data = {"on":True, "bri": midb, "xy": [color[0], color[1]]}
            requests.put(url, json=data)
        else:
            update_lights(r, g, b)
    else:
        print("Ignoring command.  This message is for ", data['array'], "and I am", LIGHT_ARRAY)







