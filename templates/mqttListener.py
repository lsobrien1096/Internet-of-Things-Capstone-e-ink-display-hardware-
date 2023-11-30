import paho.mqtt.client as mqtt
import datetime, time, sys

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm


# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# ---------------------------------------------
def on_message(client, userdata, msg):
    print("Custom Message Handler")


# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("status", 0),
                         ("lights", 0),
                         ("image_classify", 0)]
             )

# Tells the Listener to Listen Perpetually
comm.listen(on_message)




