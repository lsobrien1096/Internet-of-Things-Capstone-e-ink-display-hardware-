# USAFA Internet of Things Capstone

Raspberry Pi Gold Image Configuration
- Raspberry Pi OS (Legacy):  Available at https://www.raspberrypi.com/software/operating-systems/

Raspberry Pi Naming Convention
- rpi<model>-<room/location>-<service>
- example:  rpi0-6G141-eink

How to Clone this Repo in a Freshly Imaged Raspberry Pi (A Non-Gold Version)
- git clone https://usafaiot@github.com/usafaiot/iotcapstone
- You should clone this on the Desktop (/home/pi/Desktop)


# Configuration Details
PIP3 Packages Installed (install using sudo)
- paho-mqtt
- netifaces
- pybluez
- nanoleafapi
- lobe
- RPI.GPIO
- adafruit-blinka
- adafruit-circuitpython-bme280
- adafruit-circuitpython-ads1x15

Additional Programs to Install
- sudo apt-get install python-bluez
- sudo apt-get install fswebcam
- sudo apt-get install python3-w1thermsensor

Additional Programs to Install (Wheel Files Provided in Downloads Folder)
- sudo apt-get install numpy-1.21.4-cp37-cp37m-linux_armv7l.whl
- sudo apt-get install tensorflow-2.0.0-cp37-none-linux_armv7l.whl

Raspi-Config Settings
- Enable SPI Interface (needed for e-ink displays)
- Enable I2C Interface (needed for weather station)

Additional Commands to Run
- sudo modprobe w1-gpio
- sudo modprobe w1-therm

Modify /boot/config.txt
- Add "dtoverlay=w1-gpio" to the end of the file (without quotes)
