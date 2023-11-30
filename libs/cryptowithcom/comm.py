# -------------------------------------------
# comm.py
# MQTT Library
# -------------------------------------------
from threading import Thread
from base64 import b64encode, b64decode
import paho.mqtt.client as mqtt
import sys
import json
import datetime
import time
import crypto

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import systemInfo, rsalib

DEBUG = True
MQTT_BROKER_IP = "96.66.89.56"
CHANNELS = [ ]
MESSAGE_HANDLER = None

# MQTT Client
client = mqtt.Client()

# Specifies the amount of time before the client is forced to reconnect
# Only used when listening to channels
PERSISTENCE_CHECK_DURATION = 60.0 * 15
RECEIVED_RECENT_MESSAGE = False


# ----------------------------------------------
# Event Hander for When the Client Connects
# ----------------------------------------------
def on_connect(client, userdata, flags, rc):
    if DEBUG:
        print("MQTT CONNECTED. Subscribing to channels:", CHANNELS)
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    if len(CHANNELS) > 0:
        client.subscribe(CHANNELS)


# ----------------------------------------------
# Event Hander for When the Client Disconnects
# ----------------------------------------------
def on_disconnect(client, userdata, rc):
    if DEBUG:
        print("MQTT DISCONNECT:", client, userdata, rc, "\n")


# ----------------------------------------------
# Event Hander for When the Client Disconnects
# ----------------------------------------------
def on_message(client, userdata, msg):
    global RECEIVED_RECENT_MESSAGE
    
    # By default, we  . . .
    verified = True
    
    if DEBUG:
        print()
        print(datetime.datetime.now(), "::", "[" + msg.topic + "]", "\n", decode(msg.payload))
    
<<<<<<< HEAD
        try:
            message_contents  = json.loads(msg.payload)
            message_signature = message_contents["signature"]
            message_hostname = message_contents["hostname"]
            message_encryption = message_contents["encryption"]
            
            if message_encryption == "FERNET":
                message_contents["payload"] = crypto.decrypt_fernet(message_contents["payload"])
            else:
                print("Unknown Encryption Algorithm")
            
            msg.payload = json.dumps(message_contents)
            
            #VERIFY MESSAGE WAS SENT BY THAT PI
            verified = rsalib.verify_message(msg.payload, b64decode(message_signature), rsalib.getPublicKey(message_hostname))
            print("Message Verified:", verified)
        
        except:
            print(decode(msg.payload))
        #print("Exception")
=======
    try:
        message_contents = json.loads(msg.payload)
        
        
        
        if message_contents["encryption"] == "FERNET":
            message_contents["payload"] = crypto.decrypt_fernet(message_contents["payload"])
        else:
            print("Unknown Encryption Algorithm")
        
        msg.payload = json.dumps(message_contents)
        
        #VERIFY MESSAGE WAS SENT BY THAT PI
        verified = rsalib.verify_message(msg.payload["payload"], b64decode(msg.signature), rsalib.getPublicKey(msg.hostname))
        print("Message Verified:", verified)
        
        print("msg.payload",msg.payload)
    except:
        print(decode(msg.payload))
>>>>>>> 040fe299933550475daa49b629bfc2eb1e9eca54
    
        
    # Sets Flag to Indicate that a Message Was Received Recently
    RECEIVED_RECENT_MESSAGE = True
    
    # Forwards the Message to a Custom Handler
    if MESSAGE_HANDLER != None and verified:
        MESSAGE_HANDLER(client, userdata, msg)


# ----------------------------------------------
# Connects to the MQTT Broker
# ----------------------------------------------
def connect(destination=MQTT_BROKER_IP, channels=None):
    global CHANNELS
    
    # Updates the Channels if Needed
    if channels != None:
        CHANNELS = channels
    
    client.on_connect = on_connect
    client.connect(destination, keepalive=int(PERSISTENCE_CHECK_DURATION))
    
    
# ----------------------------------------------
# Creates a Standard MQTT Payload to Transmit
# ----------------------------------------------
def wrapMessage(payload, encrypt="FERNET"):
    now = datetime.datetime.now()
    
    if (encrypt == "FERNET"):
        #do something, encrypt the payload using a separate library
        payload = crypto.encrypt_fernet(payload)
        algorithm = "FERNET"
    elif (encrypt == "RSA"):
        pass
    else:
        algorithm = ""
    
    message = {
        "hostname":systemInfo.get_hostname(),
        "network":systemInfo.get_network(),
        "ip":systemInfo.get_ip_address(),
        "timestamp":now.strftime("%Y-%m-%d %H:%M:%S"),
        "encryption":algorithm,
        "signature":str(rsalib.sign_message("hi", rsalib.getPrivateKey())),
        #"signature":signature,
        "payload":payload
    }
    return json.dumps(message)


# ----------------------------------------------
# Sends an MQTT Message to the Broker
# This automatically wraps it with the standard
# headers
# ----------------------------------------------
def send(channel, payload, qos=0):
    
    # Wraps the payload with the standard headers
    message = wrapMessage(payload, True)
    
    
    # Sends the message on the desired channel
    client.publish(channel, message)
    
    if DEBUG:
        print("Sent Message to Broker:")
        print("  Channel:", channel)
        print("  Message:", message, "\n")


# ----------------------------------------------
# Disconnects the MQTT Client from the Broker
# ----------------------------------------------
def disconnect():
    client.disconnect()


# ----------------------------------------------
# Converts a Message (encoded in bytes)
# to a string
# ----------------------------------------------
def decode(message_in_bytes):
    return bytes.decode(message_in_bytes)


# ----------------------------------------------
# Checks to see if the connection is working
# ----------------------------------------------
def persistence_check_task():
    global RECEIVED_RECENT_MESSAGE
    
    # Assumes that the connection fails if it does not receive a message since the last persistence check
    while RECEIVED_RECENT_MESSAGE:
        print("Persistence Check PASS:  Received Message in the Past", PERSISTENCE_CHECK_DURATION, "Seconds")
        RECEIVED_RECENT_MESSAGE = False
        time.sleep(PERSISTENCE_CHECK_DURATION)
    
    print("Persistence Check FAIL:  No Message Received in the Past", PERSISTENCE_CHECK_DURATION, "Seconds")
    
    print("  - Halting Listening Loop")
    client.loop_stop()
    
    print("  - Disconnecting from the Broker")
    disconnect()
    
    print("  - Verifying Internet Connection . . . ")
    while not systemInfo.is_connected_to_internet():
        print("    - Not Connected.  Trying again in 10.0 seconds.")
        time.sleep(10.0)
    print("    - CONNECTED!")
    
    print("  - Reconnecting to the Broker")
    connect()
    
    print("  - Restarting Listening Service(s)")
    listen()
            

# ----------------------------------------------
# Creates a Thread to Listen Forever
# ----------------------------------------------
def listen_continuously_task():
    global RECEIVED_RECENT_MESSAGE
    
    # Make sure to set this so that you don't fail the test the first time
    RECEIVED_RECENT_MESSAGE = True
    
    # Tells the Listener to Listen Forever
    client.loop_forever()


# ----------------------------------------------
# Listens indefinitely for messages from the
# specified MQTT topics/channels
# ----------------------------------------------
def listen(message_handler_function = None):
    global CHANNELS, MESSAGE_HANDLER
        
    # Updates the Message Handler Function
    if message_handler_function != None:
        MESSAGE_HANDLER = message_handler_function
    
    # Creates a Thread that Listens
    listen_thread = Thread(target=listen_continuously_task)
    listen_thread.start()
    
    # Creates a Thread to Checks on the Health of the Connection
    persistence_thread = Thread(target=persistence_check_task)
    persistence_thread.start()
    

# ----------------------------------------------
# Main Script
# Initiaizates Default Values
# ----------------------------------------------

# Sets Up Event Handlers
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Verifying Internet Connection
while not systemInfo.is_connected_to_internet():
    time.sleep(2.5)

# TODO:  Verify RSA Keys Present
rsalib.generate_keys()

if DEBUG:
    print("MQTT Comm Initiaized.  Waiting for connect()")
    send("rsa_test", "{}")
    connect(MQTT_BROKER_IP,"rsa_test")
    listen(on_message)
        
    



