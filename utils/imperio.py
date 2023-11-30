import os
import requests
import sys
import json
import datetime
import time
sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import systemInfo
r = requests.post("https://iot.dfcs-cloud.net/api_v1.php", data = {
                                                            'api_key' : '12345',
                                                            'api_function' : 'getImperio',
                                                            'pi_id' : systemInfo.get_hostname()})
jsonCommand = json.loads(r.text)


command = jsonCommand['command']

if(command != None):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    commandData = {}
    commandData['pi_id'] = systemInfo.get_hostname()
    commandData['timestamp'] = timestamp
    commandData['command_response'] = "no response"
    r1 = requests.post("https://iot.dfcs-cloud.net/api_v1.php", data = {
                                                            'api_key' : '12345',
                                                            'api_function' : 'postImperio',
                                                            'data' : json.dumps(commandData)})
    print(r1.text)
    output_stream = os.popen(command)
    output = output_stream.read()
    commandData['pi_id'] = systemInfo.get_hostname()
    commandData['timestamp'] = timestamp
    commandData['command_response'] = output
    print(json.dumps(commandData))
    r2 = requests.post("https://iot.dfcs-cloud.net/api_v1.php", data = {
                                                            'api_key' : '12345',
                                                            'api_function' : 'postImperio',
                                                            'data' : json.dumps(commandData)})
    print(r2.text)
    
else:
    print("No command run")
    