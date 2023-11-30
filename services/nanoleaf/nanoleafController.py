"""
Nanoleaf Controller
Author:  Lt Col Adrian A. de Freitas
Description:  Controls a Nanoleaf Light Array
Command Line Args:  nanoleafController.py <LIGHT_ARRAY> <LIGHT_IP_ADDRESS>
"""

import time, sys, json, time, threading
from nanoleafapi import Nanoleaf, NanoleafDigitalTwin

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm

# Listener Specific Variables
LIGHT_ID = None
NANOLEAF_IP = None
LIGHT_DELAY = 1.0
lights = []
nanoleaf_all = None
nanoleaf_single = None
light_configuration = {}
configuration_updated = True


# ----------------------------------------------
# Sets Up Variables/Settings Prior to Listening
# ----------------------------------------------
def initialize():
    global LIGHT_ID, NANOLEAF_IP, lights, nanoleaf_single

    # Get Light ID
    if len(sys.argv) >= 3:
        # Use Command Line Arguments
        LIGHT_ID = int(sys.argv[1])
        NANOLEAF_IP = sys.argv[2]
        print("LIGHT_ID:", LIGHT_ID)
        print("NANOLEAF_IP:", NANOLEAF_IP)
    else:
        # Ask Questions from the User
        LIGHT_ID = int(input("Light ID: "))
        NANOLEAF_IP = input("IP Address: ")

    # Initializes Lights
    initialize_lights()

    # Creates the Auto Updating Thread
    light_update_thread = threading.Thread(target=light_updater, args=())
    light_update_thread.start()


# ----------------------------------------------
# NANOLEAF FUNCTION
# THREAD:  Updates Lights at a Set Interval
# ----------------------------------------------
def initialize_lights():
    global lights, nanoleaf_all, nanoleaf_single
    
    # Connects to the Nanoleaf Array
    print("Connecting to Nanoleaf Array at", NANOLEAF_IP)
    nanoleaf_all = Nanoleaf(NANOLEAF_IP)

    #Below object gets the information for the lights and sets them up to be individually controlled
    nanoleaf_single = NanoleafDigitalTwin(nanoleaf_all)

    #Gets light arrays from left to right and then prints the port values of them
    lights = nanoleaf_single.get_ids()
    print("Light IDs:", lights)

    # Initializes All Nanoleaf Colors to 255,255,255
    for i in range(len(lights)):
        light_configuration[lights[i]] = (255, 255, 255)
    
    nanoleaf_single.sync()


# ----------------------------------------------
# NANOLEAF FUNCTION
# THREAD:  Updates Lights at a Set Interval
# ----------------------------------------------
def light_updater():
    global configuration_updated

    try:
        while True:
            time.sleep(LIGHT_DELAY)
            if (configuration_updated == True):
                # Sets a Flag to Indicate that the Lights Haven't Been Updated
                configuration_updated = False

                # Creates a Thread to Update the Lights
                light_thread = threading.Thread(target=update_lights, args=())
                light_thread.start()

    except Exception as e:
        print("Nanoleaf Update Thread Error: ", str(e))


# ----------------------------------------------
# NANOLEAF FUNCTION
# THREAD:  Updates Lights
# ----------------------------------------------
def update_lights():
    # Creates a Debug Message
    debug_message = { "array":LIGHT_ID, "message":"Light array updated" }

    # Configures Each Light in the Entire Array
    for i in range(len(lights)):
        nanoleaf_single.set_color(lights[i], light_configuration[lights[i]])

    # Transmits the sync command
    nanoleaf_single.sync()
    print("Nanoleaf Lights Updated")

    # Transmits a Debug Message
    comm.send("nanoleaf_debug", json.dumps(debug_message))


# ----------------------------------------------
# CUSTOMIZE ME
# Converts a JSON Message to Nanoleaf Commands
# Example: { "payload": { "array":"*", "light":"*", "r":230, "g":32 , "b":104} }
# ----------------------------------------------
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
    if data['array'] == LIGHT_ID or data['array'] == "*":
        print("Processing command")
        r = int(data['r'])
        g = int(data['g'])
        b = int(data['b'])
        
        if data['light'] != '*':
            # Controlling an Individual Light
            i = int(data['light'])

            if (light_configuration[lights[i]] != (r, g, b)):
                print("Light", i, "color changed to", (r, g, b))
                light_configuration[lights[i]] = (r, g, b)
                configuration_updated = True
            else:
                print("No change to light", i)
        else:
            # Controlling all Lights in the Array
            for i in range(len(lights)):
                if (light_configuration[lights[i]] != (r, g, b)):
                    print("Light", i, "color changed to", (r, g, b))
                    light_configuration[lights[i]] = (r, g, b)
                    configuration_updated = True
                else:
                    print("No change to light", i)
    else:
        print("Ignoring command.  This message is for ", data['array'], "and I am", LIGHT_ID)


# ----------------------------------------------
# Called when MQTT Message Received
# ----------------------------------------------
def on_message(client, userdata, message):    
    message = message.payload        

    try:
        print("Processing Message:", str(message))

        # Processes the Message
        process_message(message)

        print("Processing Complete\n")

    except Exception as e:
        print("Problem Processing Message:", str(e), "\n")
        comm.send("nanoleaf_debug", { "array":LIGHT_ID, "message":"Error: " + str(e) })


# ----------------------------------------------
# Main client program
# ----------------------------------------------
print("Starting . . .")

# This is where you configure the listener
initialize()

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("lights", 0)])

# Starts Listening Indefinitely for Light Commands
comm.listen(on_message)
        
