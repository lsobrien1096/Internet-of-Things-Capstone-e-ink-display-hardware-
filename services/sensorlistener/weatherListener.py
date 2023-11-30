import paho.mqtt.client as mqtt
import datetime, time, sys, json

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm

LIGHT_CHANNEL = "lights"

# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# ---------------------------------------------
def on_message(client, userdata, msg):
    # Extracts the Headers (Formatted in JSON)
    message_contents = json.loads(msg.payload)

    # We need to test for hostname to make sure
    # this sensor is using a compatible gold version
    if "hostname" in message_contents:
        
        # Remembers the name of the device
        hostname = message_contents["hostname"]
        
        # Extracts the JSON Payload
        payload = json.loads(message_contents["payload"])
        
        # Extracts the Weather Information from the Payload
        temp = payload["temperature"]
        windspeed = payload["windspeed"]
        rainfall = payload["rainfall"]
        
        light_settings = []
                
        # RAIN Light Control
        if rainfall <= 0.2:
            light_settings.append({"array":1, "light":0, "r":0, "g":255, "b":0})
        else:
            light_settings.append({"array":1, "light":0, "r":255, "g":0, "b":0})

        # Wind Speed Light Control
        if windspeed <= 4:
            light_settings.append({"array":1, "light":1, "r":0, "g":255, "b":0})
        else:
            light_settings.append({"array":1, "light":1, "r":255, "g":0, "b":0})
             
        # Temperature Light Control
        if 60 <= temp <= 75:
            light_settings.append({"array":1, "light":2, "r":0, "g":255, "b":0})
        elif temp < 60:
            light_settings.append({"array":1, "light":2, "r":0, "g":0, "b":255})
        else:
            light_settings.append({"array":1, "light":2, "r":255, "g":0, "b":0})
        
        # Transmits Light Commands
        for light_config in light_settings:
            comm.send(LIGHT_CHANNEL, json.dumps(light_config))


# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("weather", 0)])

# Tells the Listener to Listen Perpetually
comm.listen(on_message)



