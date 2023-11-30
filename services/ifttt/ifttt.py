'''
To create an applet to work with this code, when selecting the trigger event, select the Webhooks service. Once selected,
select the "receive a web request" trigger. 

'''

import json
from pathlib import Path
import requests

event_name = "wemo2"
key = "jh7iaXuQuGQv8sCwkup34iIpelbjAMzQZZxB5Yt9_K2"
applet = "wemo2"

default_url = "https://maker.ifttt.com/trigger/" + applet + "/with/key/jh7iaXuQuGQv8sCwkup34iIpelbjAMzQZZxB5Yt9_K2"

print("Running Applet:", applet)
print("GET", default_url)
response = requests.get(default_url)
print("Task Complete:\n", response.text)



