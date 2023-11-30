from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import json, sys, os, requests, time

# Importing Standard IOT Libraries
sys.path.append("/home/pi/Desktop/iotcapstone/libs/")
import fileio, systemInfo

# Importing Waveshare E-ink Libraries
# Full Source:  https://github.com/waveshare/e-Paper
libdir  = "/home/pi/Desktop/iotcapstone/services/officesign/lib"
sys.path.append(libdir)
import epd7in5_V2

PI_ID = systemInfo.get_hostname()
API_URL = "https://iot.dfcs-cloud.net/eInkJSON.php?apiKey=12345"
DEFAULT_BACKGROUND = "/home/pi/Desktop/iotcapstone/services/officesign/CadetDorm.png"
BG_FILE = "/home/pi/Desktop/iotcapstone_data/eInk_cadetdorm.png"

FONT_DIR = "/home/pi/Desktop/iotcapstone/services/officesign/"

r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data = {'api_key' : '12345', 'api_function' : 'ro'})
data = json.loads(r.text)

lesson = data['lesson']
uod = data['uod']
weather = data['weather']
noon_meal = data['noon_meal']
m5 = data['m5']

font18 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 18)
font24 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 24)
font48 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 48)

im = Image.new('1', (800, 480), 255)

bg = Image.open(DEFAULT_BACKGROUND)
bg_width, bg_height = bg.size
w_scale = 800 / bg_width
h_scale = 480 / bg_height
im.paste(bg.resize((800, 480)), (0, 0))
draw = ImageDraw.Draw(im)
draw.text((32, 0), lesson, font = font48, fill = 0)
draw.text((32, 50), uod, font = font48, fill = 0)
draw.text((32, 100), weather, font = font48, fill = 0)
draw.text((32, 150), noon_meal, font = font48, fill = 0)
draw.text((32, 200), m5, font = font24, fill = 0)
timestamp = "(" + systemInfo.get_network() + "@" + systemInfo.get_ip_address() + ") :  "
timestamp += "Updated " + datetime.now().strftime("%B %d, %Y   %H:%M:%S")
timestamp += "Hostname: " + systemInfo.get_hostname()
time_size = font18.getsize(timestamp)
draw.text((int(800/2-time_size[0]/2), int(480-time_size[1])), timestamp, font = font18, fill = 0)

EINK = epd7in5_V2.EPD()
EINK.init()
EINK.Clear()
displaySize = (EINK.width, EINK.height)
einkImage = im

EINK.display(EINK.getbuffer(einkImage))
time.sleep(2)
EINK.sleep()




