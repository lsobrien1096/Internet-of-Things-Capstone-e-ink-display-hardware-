import sys
import time
import datetime
import requests
import json
import bluetooth._bluetooth as bt
import paho.mqtt.client as mqtt
import os

sys.path.append("/home/pi/Desktop/iotcapstone/libs/")
import comm
import bluetoothLE as ble
import fileio
import fileio, systemInfo


# Specifies how long the scan can run (in seconds)
SCAN_TIME = 3

# MQTT Settings
BLUETOOTH_CHANNEL = "bluetooth_all"

# Beacon Data
BEACON_API_URL = "https://iot.dfcs-cloud.net/bluetoothJSON.php?apiKey=12345"
BEACON_FILE = "beacons.json"
BEACON_FILE_AGE = 60.0
beacons = {}
beaconsToUpload = {}
data_to_transmit = []

# Bluetooth Socket
sock = None

# ----------------------------------------------------------
# Starts the BLE Scanner
# ----------------------------------------------------------
def start_scanner():
    global sock
    device_id = 0
    
    try:
        sock = bt.hci_open_dev(device_id)
        print("----------------------------------")
        print("Bluetooth LE Thread Started")
        print("----------------------------------")
    except:
        print ("error accessing bluetooth device...")
        sys.exit(1)
    
    ble.hci_le_set_scan_parameters(sock)
    ble.hci_enable_le_scan(sock)


# ----------------------------------------------------------
# Grabs Beacon Data from the Server
# This is Done Every X Minutes (defined by BEACON_FILE_AGE)
# ----------------------------------------------------------
def load_beacons_data():
    global beacons
    
    seconds_since_update = fileio.get_time_since_last_modified(BEACON_FILE)
    print(seconds_since_update)
    
    # Determines whether or not to get an updated beacon file from the backend
    if seconds_since_update < 0 or seconds_since_update > BEACON_FILE_AGE:
        try:
            print("Updating Beacon File")
            api_data = requests.get(BEACON_API_URL)
            fileio.write_to_file(BEACON_FILE, api_data.text)
        except Exception as e:
            print(e)
    else:
        print("Using Existing Beacon File")

    # Loads the Beacon File Into Memory
    beacons = json.loads(fileio.get_file_contents_as_string(BEACON_FILE))


# -----------------------------------------------------------
# Main Program
# -----------------------------------------------------------

# Starts the scanner
start_scanner()

# Updates the Data File Containing Beacons

#load_beacons_data()

# Calculates the Times when the Scan is Supposed to Occur
currentDate = datetime.datetime.now()
stopDate = datetime.datetime.now() + datetime.timedelta(seconds=SCAN_TIME)

beaconsReported = {}

# Sometimes, a beacon is detected multiple times in a scan session
# so this loop basically ignores duplicate entries 
while currentDate < stopDate:
    # Retrieves the Beacons Found
    beaconsFound = ble.parse_events(sock, 10)
    print(beaconsFound)   
    for beacon in beaconsFound:
        beaconAttributes = beacon.split(",")
        
        beaconID = beaconAttributes[1]
        beaconRSSI = beaconAttributes[-1]
        beaconTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        beaconsReported[beaconID] = (beaconID, beaconRSSI, beaconTime)
            
    currentDate = datetime.datetime.now()
        
print("\n\n-------------------------------------------------")
print("Scan Completed at ", currentDate)
print("-------------------------------------------------")
print("Found " + str(len(beaconsReported)) + " unique devices\n")

load_beacons_data()
# Only reports data for beacons that we are looking for
for beaconID in beaconsReported:
    if beaconID in beacons["BEACON"]:
        # Gets the Index of the Beacon
        beacon_index = beacons["BEACON"].index(beaconID)

        # Gets Information About the Beacon
        beacon_owner    = beacons["OWNER"][beacon_index]
        beacon_location = beacons["LOCATION"][beacon_index]
        beacon_rssi     = beacons["RSSI"][beacon_index]
        beacon_time     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        beaconsToUpload["BEACON"] = beaconID
        beaconsToUpload["RSSI"] = beacon_rssi
        beaconsToUpload["TIMESTAMP"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        beaconsToUpload["PI_ID"] = systemInfo.get_hostname()

        print("Found:", beacon_owner, beaconID, beacon_rssi)
         


        
        # Connects to the MQTT Broker
        comm.connect()

        # Transmits the Data
        comm.send(BLUETOOTH_CHANNEL, beaconsToUpload)

        # Disconnects from the MQTT Broker
        comm.disconnect()

