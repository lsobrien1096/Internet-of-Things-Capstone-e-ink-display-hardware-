import requests, time, math, json



import paho.mqtt.client as mqtt
import datetime, time, sys

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm

def jays_function(client, userdata, message):
    print(message.payload)
    

# -----------------------  ---------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("charleshouse", 0)])

# Tells the Listener to Listen Perpetually
comm.listen(jays_function)




#comm.send("charleshouse", {"payload":"hello jay is watching"})

