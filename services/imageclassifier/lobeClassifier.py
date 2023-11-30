# ------------------------------------------------------------------------
# Generic Lobe Tensorflow Classifier
# https://github.com/lobe/lobe-python
# ------------------------------------------------------------------------
from lobe import ImageModel
import sys, os, json, time

sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm
import fileio

# SETTINGS
TENSOR_MODELS = []
SENSING_FREQUENCY_IN_SECONDS = 60.0
SENSOR_CHANNEL = "image_classify"
IMAGE_FILENAME = fileio.get_filename("lobe_image.jpg")


# -----------------------------------------------------
# Takes a Photo from the Default Webcam
# -----------------------------------------------------
def take_photo():
    # Runs the command to take a photo
    cmd = 'fswebcam -S 10 -r 1280x720 --no-banner ' + IMAGE_FILENAME
    os.system(cmd)


# -----------------------------------------------------
# Identify prediction and turn on appropriate LED
# -----------------------------------------------------
def report(channel, model_name, label):
    comm.send(channel, {"model":model_name, "label":label})
    

# -----------------------------------------------------
# Main Program
# -----------------------------------------------------
comm.connect()

# Gets Model(s) from the command line argument
if len(sys.argv) > 2:
    SENSING_FREQUENCY_IN_SECONDS = float(sys.argv[1])
    
    for i in range(2, len(sys.argv)):
        print("\nLoading Tensorflow (Lite) Model", sys.argv[i])
        model = ImageModel.load(sys.argv[i])
        TENSOR_MODELS.append((sys.argv[i], model))
        print("COMPLETE!\n")
else:
    print("Expected:  <REFRESH_RATE_IN_SECONDS> <MODEL_1> <MODEL_2> ...")
    exit(1)


# Continuously Takes Photos and Classifies Them
while True:
    take_photo()
    for i in range(len(TENSOR_MODELS)):
        result = TENSOR_MODELS[i][1].predict_from_file(IMAGE_FILENAME)
        print("Model", TENSOR_MODELS[i][0], "classified image as label", result.prediction)
        report(SENSOR_CHANNEL, TENSOR_MODELS[i][0], result.prediction)
        
    time.sleep(SENSING_FREQUENCY_IN_SECONDS)
    

comm.disconnect()