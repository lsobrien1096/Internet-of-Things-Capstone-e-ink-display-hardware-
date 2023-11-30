#Nanoleaf Documentation

## How to hard-reset the Nanoleaf
If nothing is working at all on the nanoleaf it may require a hard reset. To do that, unplug the controller (square that has buttons on it)
press down on the power and brighter button and plug the controller back in. Wait until the button lights turn on and start cycling (the nanoleaf
is rebooting at this point). Once the light starts showing colors, it is ready to pair. Connect to the light on your phone and make sure you are
on the wifi network that you want to use for the light.

## Connecting the Nanoleaf to the MQTT
Find the IP Address on the light you are trying to use. On a raspberry pi, cd to the nanoleaf folder. Then run "sudo python3 nanoleafController.py
number ip_address". In this command the number is the light id and the ip address is the ip of the nanoleaf.
Once the raspberry pi is connected to the light, it will listen fo the MQTT lights channel. 

## Updating the color of the Lights
The nanoleaf is listening on the lights channel of the MQTT. To change the color of the lights an example payload needs to be on the MQTT:
{ "payload": { "array":"*", "light":"*", "r":230, "g":32 , "b":104} } .
