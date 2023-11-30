# Import libraries

from PIL import Image
import cv2
import numpy as np
import requests
import json
import time
import calendar
import os
import sys

# This Gives this Script Access to the Libs Folder
sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect()


def processImage(picName):
    # Reading image by name
    image = Image.open(picName)
    image = image.resize((450,250))
    image_arr = np.array(image)

    grey = cv2.cvtColor(image_arr,cv2.COLOR_BGR2GRAY)
    Image.fromarray(grey)

    blur = cv2.GaussianBlur(grey,(5,5),0)
    Image.fromarray(blur)

    dilated = cv2.dilate(blur,np.ones((3,3)))
    Image.fromarray(dilated)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
    Image.fromarray(closing)
    
    return closing


def takePicture():
        # take picture
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    picName = "parkingLot" + str(time_stamp) + ".jpg"
    command = "libcamera-still -o " + picName
    os.system(command)
    return picName


def classify_objects(model_filename, image):
    model = cv2.CascadeClassifier(model_filename)
    objects = model.detectMultiScale(image, 1.1, 1)
    return objects


def process_objects(objects):
    cnt = 0

    print("Objects Found:")
    print(objects)

    for (x,y,w,h) in objects:
      cv2.rectangle(image_arr,(x,y),(x+w,y+h),(255,0,0),2)
      cnt += 1
    
    if( cnt < 4 ):
        comm.send("parking", 0)
        print("Parkinglot Full\n")
    else:
        comm.send("parking", cnt)
        print(cnt, " spots available!\n")


# -----------------------------------
# Main program starts here
# -----------------------------------
if len(sys.argv) <= 1:
    print("USAGE:  classify.py model_name (optional)filename")

elif len(sys.argv) == 2:
    print("CONTINUOUS PHOTO MODE")
    while True:
        picName = takePicture()
        processedImaged = processImage(picName)
        objects = classify_objects(sys.argv[1], processedImage)    

        process_objects(objects)
        
        #Image.fromarray(image_arr)
        time.sleep(600)

elif len(sys.argv) == 3:
    print("PROVIDED PHOTO MODE")
    
    picName = sys.argv[2]
    processedImage = processImage(picName)
    objects = classify_objects(sys.argv[1], processedImage)    
    
    process_objects(objects)
    