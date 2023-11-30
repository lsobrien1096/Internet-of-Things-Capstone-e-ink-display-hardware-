# -------------------------------------------
# systemInfo.py
# Collects Information About this Device
# -------------------------------------------
import socket
import subprocess
import netifaces
import requests


# ----------------------------------------------
# Returns the Device's Hostname
# ----------------------------------------------
def get_hostname():
    return socket.gethostname()


# ----------------------------------------------
# Returns the Device's Current IP Address
# ----------------------------------------------
def get_ip_address():
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        if interface != "lo" and netifaces.AF_INET in addrs:
            return str(addrs[netifaces.AF_INET][0]['addr'])
        
    return "UNKNOWN"


# ----------------------------------------------
# Returns the Network Name that this Device is Connected To
# ----------------------------------------------
def get_network():
    try:
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if interface != "lo" and netifaces.AF_INET in addrs:
                if (interface == "eth0"):
                    return "ETHERNET"
                else:
                    return subprocess.check_output(['/usr/sbin/iwgetid']).decode("utf-8").split(":")[-1].replace("\"", "").strip()
    except Exception as e:
        print("Error Getting Network:", e)
    
    # Default Response
    return "UNKNOWN"


# ----------------------------------------------
# Verifies Internet Connection
# Returns True or False
# ----------------------------------------------
def is_connected_to_internet():
    url = "http://www.google.com"
    timeout = 5
    try:
        print("Checking for Internet Connection . . . ", end='')
        request = requests.get(url, timeout=timeout)
        print("Connected!")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No Connection Detected")
        return False