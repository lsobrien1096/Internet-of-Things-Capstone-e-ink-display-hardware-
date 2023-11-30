
import time
import calendar
import os



while True:
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    name = "parkingLot" + str(time_stamp) + ".jpg"
    command = "libcamera-still -o " + name
    os.system(command)
    time.sleep(600)
