Hue Documentation

## Set Up the Hue
Follow steps on this link to get the bridge and lights working
Should be easy enough: https://developers.meethue.com/develop/get-started-2/

## Controlling the Hue
Send a payload on the MQTT Lights channel following the format below.
{ "payload": { "array":"*", "light":"*", "r":230, "g":32 , "b":104} }

## Running the Hue
python3 huecontroller.py
Light Array: 1
IP Address: ex. 10.0.0.146
Hue API Key: ex. 14rsqBh25OQBcnpBuFEWfvmYsIryXcyuKcNWu3XW
