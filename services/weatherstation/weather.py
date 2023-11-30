# -----------------------------------
# Raspberry Pi Weather Station
# YOU MUST ENABLE ARM I2C INTERFACE IN RASPI-CONFIG
# -----------------------------------

# Documentation Available at
# http://bc-robotics.com/tutorials/raspberry-pi-weather-station-part-2/

# Troubleshooting Issue (I2C Interface)
# https://github.com/timofurrer/w1thermsensor/issues/42

# Imports Standard Raspberry Pi Libraries
import RPi.GPIO as GPIO
import board, busio, json, sys, time

# Imports Weather Sensor Libraries
from w1thermsensor import W1ThermSensor
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1015 as ADS
from adafruit_bme280 import basic as adafruit_bme280

# Imports Custom IOT Capstone Libraries
sys.path.append("/home/pi/Desktop/iotcapstone/libs/")
import comm

# MQTT Channel Used to deliver MQTT Data
MQTT_CHANNEL = "weather"

# Used to count the number of times the wind speed input is triggered
windTick = 0

# Used to count the number of times the rain input is triggered
rainTick = 0

# How long we want to wait between loops (seconds)
interval = 15

# Contains the Information We Will Send to the Server
weather_data = {}

# Event for when the wind sensor is triggered
def windtrig(self):
    global windTick
    windTick += 1
    print("EVENT:  Wind Sensor Triggered (windTick =", str(windTick) + ")")
    
# Event for when the rain sensor is triggered
def raintrig(self):
    print("EVENT:  Rain Sensor Triggered")
    rainTick += 1
    print("EVENT:  Rain Sensor Triggered (rainTick =", str(windTick) + ")")

# Converts an analog value from the wind direction sensor
# into a wind direction
def get_wind_direction(val):
    windDir = "UNKNOWN"
    windDeg = -1
    
    if 20000 <= val <= 20500:
        windDir = "N"
        windDeg = 0

    if 10000 <= val <= 10500:
        windDir = "NNE"
        windDeg = 22.5

    if 11500 <= val <= 12000:
        windDir = "NE"
        windDeg = 45

    if 2000 <= val <= 2250:
        windDir = "ENE"
        windDeg = 67.5

    if 2300 <= val <= 2500:
        windDir = "E"
        windDeg = 90

    if 1500 <= val <= 1950:
        windDir = "ESE"
        windDeg = 112.5

    if 4500 <= val <= 4900:
        windDir = "SE"
        windDeg = 135

    if 3000 <= val <= 3500:
        windDir = "SSE"
        windDeg = 157.5

    if 7000 <= val <= 7500:
        windDir = "S"
        windDeg = 180

    if 6000 <= val <= 6500:
        windDir = "SSW"
        windDeg = 202.5

    if 16000 <= val <= 16500:
        windDir = "SW"
        windDeg = 225

    if 15000 <= val <= 15500:
        windDir = "WSW"
        windDeg = 247.5

    if 24000 <= val <= 24500:
        windDir = "W"
        windDeg = 270

    if 21000 <= val <= 21500:
        windDir = "WNW"
        windDeg = 292.5

    if 22500 <= val <= 23000:
        windDir = "NW"
        windDeg = 315

    if 17500 <= val <= 18500:
        windDir = "NNW"
        windDeg = 337.5

    return windDir


# ---------------------------------------------------
# STEP 1:  Setup Pi to Use Hardware
# ---------------------------------------------------
# Gets a Reference to the BME280 Chip
i2c = busio.I2C(board.SCL, board.SDA)
bme = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Gets a Reference to the ADS1015 Board (wind direction)
ads = ADS.ADS1015(i2c)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)

# Gets a Reference to the Thermal Probe
ds18b20 = W1ThermSensor()

# Set GPIO pins to use BCM pin number4
GPIO.setmode(GPIO.BCM)
 
# Set digital pin 17 to an input and enable the pullup 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
# Set digital pin 23 to an input and enable the pullup 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
# Register Event Handler to detect wind (4 ticks per revolution)
GPIO.add_event_detect(17, GPIO.BOTH) 
GPIO.add_event_callback(17, windtrig)
  
# Register Event Handler to detect rainfall tick
GPIO.add_event_detect(23, GPIO.FALLING)
GPIO.add_event_callback(23, raintrig)

# Prepares MQTT Connection
comm.connect()

# ---------------------------------------------------
# STEP 2:  Collect Data
# Primarily for Wind / Rain; Others are Instantaneous
# ---------------------------------------------------
print("Sampling Weather Sensors for", interval, "seconds")
time.sleep(interval)
print("Sampling Complete!\n")


# ---------------------------------------------------
# STEP 3:  Calculate Weather Data
# ---------------------------------------------------
# Pull Temperature from DS18B20 (in C)
temperature = ds18b20.get_temperature()

# Convert temperature to F
weather_data["temperature"] = round(temperature * (9/5) + 32, 1)

# Pull pressure from BME280 Sensor & convert to kPa
pressure_pa = bme.pressure
weather_data["pressure"] = round(pressure_pa / 10, 1)

# Pull humidity from BME280 (Units = Percentage)
weather_data["humidity"] = round(bme.humidity, 1)

# Calculate wind direction based on ADC reading
val = chan.value
weather_data["wind_direction"] = get_wind_direction(val)

# Calculate average windspeed
# A wind speed of 1.2km/h will cause this switch to open or close once per second.
# So we just need to count how many times it is opening and closing per second to figure out a speed.
# NOTE:  To convert from kph to mph, divide kph by 1.609
windspeed_in_kph = (windTick * 1.2) / interval
weather_data["windspeed"] = round(windspeed_in_kph / 1.609, 1)

# Calculate accumulated rainfall
# Each tick represents 0.2794mm of rainfall
# NOTE:  To convert to inches, divide mm by 25.4
rainfall_in_mm = rainTick * 0.2794
weather_data["rainfall"] = round(rainfall_in_mm / 25.4, 1)


# ---------------------------------------------------
# STEP 4:  Transmit the Weather Data to the MQTT Broker
# ---------------------------------------------------
#print(weather_data)
comm.send(MQTT_CHANNEL, json.dumps(weather_data))

# Disconnects the MQTT Connection
comm.disconnect()
print("Weather Station Complete")

#raise SystemExit


