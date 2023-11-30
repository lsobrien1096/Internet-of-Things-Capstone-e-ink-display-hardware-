# Weather Station Documentation

### How to Set Up a Raspberry Pi to Act as a Weather Station
The first step is to ensure the pi has internet connectivity and setting up the pi to be able to interact with the weather station hardware. First up, 
the Adafruit Python GPIO Library and the Adafruit BME280 library need to be installed. The BME280 is specifically designed to work with the pressure and humidity
sensors on the weather station. After this, we need to install the ADS1x15 library to read the wind direction and set up the DS18B20 sensor to read the
temperature. Now we've configured our hardware, we can write some Python code that will interact and communicate with the hardware and poll the
weather station incrementally for data.

### How the Pi Communicates With the Weather Hardware
After completing the setup above, the pi communicates with the weather hardware using functions that are built into the respective libraries. 
For the temperature, the library for the DS18B20 temperature sensor contains a function to pull the current temperature reading called get_temperature, so this library must
be imported, and after doing so, we can get the temperature reading. Now, we pull the pressure and humidity using the BME280. Once again, we must import the library to be able to
access the functions specific to the BME280, in this case bme.pressure and bme.humidity. It is important to note that the temperature reading from the DS18B20 will be in Celsius,
so a conversion to Fahrenheit is necessary. The pressure reading from the BME280 should also be converted from pa to kPa for ease of use. Wind direction is the hardest data to 
collect; each different wind direction outputs a voltage within a specific range. For example, a wind direction of North results in a voltage value between 20000 and 20500, NNE is
between 10000 and 10500. We must include the range for each of the 16 directions in order to interpret the reading accurately. To calculate wind speed, the number of times
the wind sensor is triggered within the sampling period must be recorded using the windTick variable, and then converted from kph to mph for ease of use. And finally for rainfall,
the sensor contains a small tipping device that switches back and forth every 0.2794mm of rainfall, so the number of times this switches back and forth is counted using the 
rainTick variable and then multiplied by 0.2794 to get our reading. This must also be converted from mm to inches. 

### How the Pi Reports Weather Data
The Python program is set to run on a 15-second interval, meaning it will sample the weather sensors for 15 seconds every 5 minutes (which is how often the server refreshes). 
However, you can also manually run the code and take a weather reading that way as well. Using GPIO on the pi, the pi sends out a signal to the weather station to collect data and 
the data is transmitted back to the pi. Once all the necessary data has been collected, the pi sends the data to the server over MQTT.

### Light Connectivity
There is also a program running that will inform the Nanoleaf lights what colors to display based on the current weather data. For example, if the temperature is between
60 and 75 degrees farenheit, the lights will display green. If the temperature is less than 60, they will display blue, and etc. There are also similar conditionals for the
amount of rainfall measured and the windspeed. 
