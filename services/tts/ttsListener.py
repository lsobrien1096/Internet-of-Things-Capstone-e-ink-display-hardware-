import paho.mqtt.client as mqtt
import datetime, time, sys, json
from pydub import AudioSegment
from pydub.playback import play
 
sys.path.append("/home/pi/Desktop/iotcapstone/libs")
import comm

from num2words import num2words
from subprocess import call

# ---------------------------------------------
# Event Handler for When the Client Gets an MQTT Message
# ---------------------------------------------
def on_message(client, userdata, message):
    message = message.payload        

    # Extracts the Headers (Formatted in JSON)
    message_contents = json.loads(message)
    print(message_contents)

    print(message_contents['payload'])
    data = str(message_contents['payload'])

    try:
        print("Processing Message:", str(data))

        # Processes the Message
        tts(str(data))
        print("Processing Complete\n")

    except Exception as e:
        print("Problem Processing Message:", str(e), "\n")


def playWAV(filename):
    song = AudioSegment.from_wav(filename)
    play(song)


def tts(message):
    if (message == 'meow'):
        playWAV('meow.wav')
    elif (message == 'door'):
        playWAV('doortrek.wav')
    else:        
        cmd_beg= 'espeak -ven-f2'
        cmd_end= ' | aplay /home/pi/Desktop/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
        cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file

        text = message
        print(text)

        #Replacing ' ' with '_' to identify words in the text entered
        text = text.replace(' ', '_')

        #Calls the Espeak TTS Engine to read aloud a Text
        call([cmd_beg+cmd_out+text+cmd_end], shell=True)
    
# --------------------------------------------
# Main Program
# --------------------------------------------

# Connects to the MQTT Broker and starts listening to the following channels
comm.connect(channels = [("tts", 0)])

# Tells the Listener to Listen Perpetually
comm.listen(on_message)





