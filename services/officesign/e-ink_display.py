# --------------------------------------------------
# E-Ink "Smart Sign" Display Service
# NOTE:  Must Enable SPI in rpi-config
#        (in Interfacing Options)
# --------------------------------------------------

# Importing System Libraries
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

# Set Configuration Details
PI_ID = systemInfo.get_hostname()
PI_LOCATION = "location" 

# Stores EInk Display Contents
DATA_FILE = "/home/pi/Desktop/iotcapstone_data/eInk_Data.txt" #eInk display data

# Stores Default Images
DEFAULT_BACKGROUND = "/home/pi/Desktop/iotcapstone/services/officesign/eInk_background_default.png"
DEFAULT_IMAGE = "/home/pi/Desktop/iotcapstone/services/officesign/eInk_image_default.png"

# Stores the Folder where Font Data is Contained
FONT_DIR = "/home/pi/Desktop/iotcapstone/services/officesign/"

# Important URLs / Credentials
API_URL       = "https://iot.dfcs-cloud.net/eInkJSON.php?apiKey=12345"
API_LOGIN_URL = "https://iot.dfcs-cloud.net/login.php"
API_USERNAME  = "2021Cap"
API_PASSWORD  = "grindn3v3rstops"
PIC_URL       = "https://iot.dfcs-cloud.net/"


# E-INK DISPLAY CONTENTS
DISPLAY_WIDTH = 0 #set later
DISPLAY_HEIGHT = 0 #set later
   
# Fonts Used to Render the Size
font18 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 18)
font24 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 24)
font48 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 48)

# CONSTANT Value that indicates where the custom image is located
LOCAL = "LOCAL" 
 
# CONSTANT Values that indicate privacy settings
NONE = "NONE" #don't show any location info
BASIC = "BASIC" #show only here or away based on BT data
FULL = "FULL" #show exact location based on BT data


# -------------------------------------------
# Generates Default eInk Settings
# -------------------------------------------
def load_default_configuration():
    # This represents the default values of the eInk Display
    dictionary = {
        "BG_FILE": "/home/pi/Desktop/iotcapstone_data/eInk_background.png",
        "NAME": "E-Ink Display",
        "FILE PATH": "images/einkimages/eInk_Default.png",
        "IMAGE_FILE": "/home/pi/Desktop/iotcapstone_data/eInk_image.png",
        "LOCATION": "SETUP MODE",
        "MESSAGE": "Make sure that PI_ID: " + PI_ID + " is registered at https://iot.dfcs-cloud.net \n1. Scan the QR code and register your account \n2. Update all fields of your sign. Give the image upload time to complete if it is a large image.\n3. Input the PI_ID exactly how it is show on this display\n4. Wait for the sign to update and enjoy!",
        "PICTURE": "WEB",
        "PRIVACY": "FULL",
        "TITLE": "PI_ID: " + PI_ID,
        "NETWORK": True
    }
    
    # Generates the System Files if they Don't Exist
    if fileio.file_exists(DATA_FILE) == False:
        print("Cannot Find Data File", DATA_FILE, ". . . Creating from Scratch")
        fileio.write_to_file(DATA_FILE, json.dumps(dictionary))

    if fileio.file_exists(dictionary["BG_FILE"]) == False:
        print("Cannot Find Image File", dictionary["BG_FILE"], ". . . Loading Default")
        fileio.copy_file(DEFAULT_BACKGROUND, dictionary["BG_FILE"])

    if fileio.file_exists(dictionary["IMAGE_FILE"]) == False:
        print("Cannot Find Image File", dictionary["IMAGE_FILE"], ". . . Loading Default")
        fileio.copy_file(DEFAULT_IMAGE, dictionary["IMAGE_FILE"])

    return dictionary


# ---------------------------------------------------
# Examines the output by the web service and
# determines which entry is associated with this eInk
# ---------------------------------------------------
def extract_configuration(raw):
    global PI_LOCATION
    
    data = json.loads(raw)
    for index in range(0, len(data[list(data.keys())[0]])):
        dictionary = {}
        for key in data.keys():
            if key=="ID":
                #dictionary[key] = "eInk_Pi" + str(data[key][index]).zfill(7) #IDs are saved in the database as numbers, so we need to add the eInkPi identifier
                dictionary[key] = data[key][index]
            else:
                dictionary[key] = data[key][index]

        PI_LOCATION = dictionary["LOCATION"]

        if dictionary["ID"] == PI_ID:
            return dictionary
    
    print("eInk", PI_ID, "does not appear to have an entry in the database")
    dir = '/home/pi/Desktop/iotcapstone_data/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    load_default_configuration()
    EINK_CURRENT_DATA = fileio.get_file_contents_as_json(DATA_FILE)
    render_sign_contents()

    exit(1)
       
# -------------------------------------------
# Return true or false if values of identical keys do not match
# -------------------------------------------
def dictionaries_different(dict_from_file, dict_from_web):
    
    # We are only concerned if there a key in the web dictionary
    # does not match a value in the file
    for key in list(dict_from_file.keys()):
        if key in list(dict_from_web.keys()):
            #check if file matches web
            if dict_from_file[key] != dict_from_web[key]:
                print("DICTIONARIES ARE DIFFERENT:", key)
                print("  - Dictionary A:", dict_from_file[key])
                print("  - Dictionary B:", dict_from_web[key])
                return True   
    
    print("DICTIONARIES ARE EQUIVALENT", "\n")
    return False


# -------------------------------------------
# Update with data from another dictionary
# -------------------------------------------
def update_configuration(existing_dictionary, new_dictionary):
    final_dict = {}
    
    # Updates Everything in the Existing Dictionary
    # with Values from the New Dictionary
    for k in existing_dictionary.keys():
        if k in new_dictionary.keys():
            final_dict[k] = new_dictionary[k]
        else:
            final_dict[k] = existing_dictionary[k]
    
    # Adds Key/Value Pairs that are in the New Dictionary
    # but Not Currently in the Existing Dictionary
    for k in new_dictionary.keys():
        if k not in existing_dictionary.keys():
            final_dict[k] = new_dictionary[k]
            
    return final_dict


# ------------------------------------------------
# Saves the Current State of the Sign to a Text File
# So that we can remember what it looks like in future runs
# ------------------------------------------------
def save_configuration():
    fileio.write_to_file(DATA_FILE, json.dumps(EINK_CURRENT_DATA))


# ------------------------------------------------
# Obtains the image selected by the user in the
# database
# ------------------------------------------------
def get_picture(path):
    global IMAGE_FILE
    
    session_requests = requests.session()
    
    # Get login csrf token
    #result = session_requests.get(API_LOGIN_URL)

    # Create payload
    #payload = { "username":API_USERNAME, "password":API_PASSWORD }

    # Perform login
    #result = session_requests.post(API_LOGIN_URL, payload)

    # Downloads the Image
    result = session_requests.get(PIC_URL+path)
    
    # Extracts the URL from the Path
    f_ext = path.split(".")[-1].strip().lower()
    
    # Writes the Image to a File (for supported file types)
    if f_ext in {"jpg", "jpeg", "png", "bmp"}:
        IMAGE_FILE = IMAGE_FILE.split(".")[0] + "." + f_ext
        with open(IMAGE_FILE, 'wb') as f:
            f.write(result.content)
    else:
        raise Exception("Unsupported file type: " + f_ext)


# ------------------------------------------------
# Creates an image containing the sign contents
# ------------------------------------------------
def create_sign(name, title, message, location, picture, size):    
    print("----------------------------------------------------")
    print("Size:    ", size)
    print("Name:    ", name)
    print("Picture: ", picture)
    print("Location:", location)
    print("Title:   ", title)
    print("Message: ")
    print(message)
    print("----------------------------------------------------")
    
    print("Generating background . . .", end=' ')
    
    # Creates a Blank Image (255 == White)
    im = Image.new('1', (size[0], size[1]), 255)
    
    # Loads and Displays the Background
    bg = Image.open(BG_FILE)
    bg_width, bg_height = bg.size
    w_scale = size[0] / bg_width
    h_scale = size[1] / bg_height
    im.paste(bg.resize((size[0], size[1])), (0, 0))
    draw = ImageDraw.Draw(im)
    
    print("SUCCESS!")
    
    # Profile Image (e.g., the image that the user uploads to the website)
    print("Obtaining profile image . . .", end=' ')
    
    if picture != LOCAL:
        try:
            get_picture(EINK_CURRENT_DATA["FILE PATH"]) #download picture from web
            
            EINK_CURRENT_DATA["IMAGE_FILE"] = IMAGE_FILE
            EINK_CURRENT_DATA["PICTURE"] = LOCAL
            
            save_configuration()
            print("DOWNLOADED NEW FILE SUCCESSFULLY!")
            
        except Exception as e:
            print("FAILED")
            print(e)
    else:
        print("USING EXISTING FILE!")
        
    # Drawing the Image
    print("Drawing profile image . . .", end=' ')
    
    try:
        pic_x = 25      # picture x location
        pic_y = 104     # picture y location
        pb_width = 280  # picture width
        pb_height = 346 # picture height
        
        pic = Image.open(IMAGE_FILE)
        im.paste(pic.resize((int(pb_width*w_scale),int(pb_height*h_scale))), (int((pic_x+1)*w_scale),int((pic_y+1)*h_scale)))
        draw = ImageDraw.Draw(im)
        print("SUCCESS!")
        
    except Exception as e:
        print("FAILED!")
        print(e)
     
    # Text Contents
    print("Drawing sign text . . .", end=' ')
    
    try:
        # Name and title
        draw.text((32, 0), name, font = font48, fill = 0)
        draw.text((36, 50), title, font = font24, fill = 0)
         
        #Message
        num_lines = 17 #the textbox can fit 17 lines 
        line_size = 20 #lines are 20 pixels
        tb_x = 330 #textbox x location
        tb_y = 108 #textbox y location
        tb_width = 440 #textbox width
        line_number = 0
        message = message.replace("\r", "")
        message_array = message.split("\n")
        
        for text in message_array:
            text = text + " "
            chars_remaining = len(text)
            line_start = 0
            line_end = chars_remaining
            #print(font18.getsize(message[line_start:line_end])[0])
            while chars_remaining > 0:
                while font18.getsize(text[line_start:line_end])[0] > tb_width:
                    line_end = line_end-1
                #line is correct length
                #backtrack lo last space
                #print(message[line_end-1])
                temp = line_end
                while text[line_end-1] != " ":
                    line_end = line_end-1
                    if line_end == -1:
                        line_end = temp
                        break
                line = text[line_start:line_end] + " "
                draw.text((tb_x, tb_y+line_number*line_size), line, font = font18, fill = 0)
                line_start = line_end
                chars_remaining = chars_remaining - len(line)
                line_end = line_end + chars_remaining + 1
                line_number = line_number+1
                
                if line_number == num_lines:
                    chars_remaining = 0
            
            # Stops Drawing Text if No More Room
            if line_number == num_lines:
                break
            
        print("SUCCESS!")
    
    except Exception as e:
        print("FAILED!")
        print(e)

    # Beacon Location
    if PRIVACY==FULL:
        #show full location data
        loc = location
    elif PRIVACY==BASIC:
        #show basic location data (here or away)
        if location==PI_LOCATION:
            loc = "Here"
        else:
            loc = "Away"
    else:
        #do not show location
        loc = ""
    
    draw.text((600, 10), loc, font = font24, fill = 0)
    
    # Network & Update Timestamp
    if "NETWORK" in EINK_CURRENT_DATA:
        timestamp = "(" + systemInfo.get_network() + "@" + systemInfo.get_ip_address() + ") :  "
    else:
        timestamp = "(NO NETWORK):  "
        
    timestamp += "Updated " + datetime.now().strftime("%B %d, %Y   %H:%M:%S")
    timestamp += "Hostname: " + systemInfo.get_hostname()
    time_size = font18.getsize(timestamp)
    draw.text((int(size[0]/2-time_size[0]/2), int(size[1]-time_size[1])), timestamp, font = font18, fill = 0)
    
    # Returns the Sign so that it can be drawn
    print("Sign Successfully Rendered")
    return im

# -------------------------------------------
# Displays the Contents of the Sign
# -------------------------------------------
def render_sign_contents():
    try:
        # Gets eInk Object
        EINK = epd7in5_V2.EPD()
        EINK.init()
        EINK.Clear()
        displaySize = (EINK.width, EINK.height)
        
        # Creates the Image to be Displayed
        einkImage = create_sign(EINK_CURRENT_DATA["NAME"],
                                EINK_CURRENT_DATA["TITLE"],
                                EINK_CURRENT_DATA["MESSAGE"],
                                EINK_CURRENT_DATA["LOCATION"],
                                EINK_CURRENT_DATA["PICTURE"],
                                displaySize)
        
        # Updates the Display with the Newly Created Image
        EINK.display(EINK.getbuffer(einkImage))
        
        # Puts the Sign Into Rest Mode for the Next Update
        # I think.  I really don't know why
        time.sleep(2)
        EINK.sleep()

    except Exception as e:
        print("Error initializing eInk display:", e)
        print("Make sure the sign is connected and SPI is enabled in rpi-config")
        epd7in5_V2.epdconfig.module_exit()

 
# ---------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------

# Loads the Default Configuration (and creates files if needed)
load_default_configuration()

# Loads the eInk Data File
EINK_CURRENT_DATA = fileio.get_file_contents_as_json(DATA_FILE)
BG_FILE = EINK_CURRENT_DATA["BG_FILE"]
IMAGE_FILE = EINK_CURRENT_DATA["IMAGE_FILE"]
PRIVACY = EINK_CURRENT_DATA["PRIVACY"]

try:
    network_restored = False
    
    # Step 1:  Get JSON from the webservice that contains the file contents
    # NOTE:  The previous team's webservice returns it for EVERY sign.  Yuck . . .
    try:
        print("\nUSING WEB SERVICE:")
        print(API_URL, "\n")
        
        session_requests = requests.session()
        result = session_requests.get(API_URL)
        webserver_data = extract_configuration(result.text)
        
        # Sets a Flag Indicating if the Network was Restored
        if "NETWORK" not in EINK_CURRENT_DATA:
            network_restored = True
        
        # Sets a Flag Stating that the Network Works
        EINK_CURRENT_DATA["NETWORK"] = True
        
    except Exception as e:
        print("Problem occurred while trying to contact web server:", e, "\n")
        
        print("USING CURRENT E-INK DATA:")
        print(EINK_CURRENT_DATA)
        print()
        
        # Only Renders During the First Detection of a Network Outage
        if "NETWORK" in EINK_CURRENT_DATA:
            
            # Removes the Flag Stating that the Network Works
            del EINK_CURRENT_DATA["NETWORK"]
                        
            # Saves the File to Memory
            save_configuration()
                    
            print("\nRendering Sign (Disconnected Mode):")
            render_sign_contents()
                
        else:
            print("Need to Update Sign (Disconnected Mode)? NO", "\n") 

    print("NETWORK RESTORED:")
    print(network_restored, "\n")

    # Step 2:  See if the dictionary obtained in the previous step is different
    if "NETWORK" in EINK_CURRENT_DATA or network_restored == True:
        print("CURRENT E-INK DATA:")
        print(EINK_CURRENT_DATA)
        print("\nWEBSITE DATA:")
        print(webserver_data)
        print()
        
        # Will update the sign if the data changed, or network status changed between runs
        if dictionaries_different(EINK_CURRENT_DATA, webserver_data) or network_restored == True:
            print("Need to Update Sign? YES")
            
            # Determines whether or not we can use the local image
            # or if we need to download something else
            if EINK_CURRENT_DATA["FILE PATH"] != webserver_data["FILE PATH"]:
                EINK_CURRENT_DATA["PICTURE"] = "WEB"
            
            # Updates the Rest of the Eink Current Dictionary
            EINK_CURRENT_DATA = update_configuration(EINK_CURRENT_DATA, webserver_data)
                                             
            # Saves the Sign's Current State to Memory
            save_configuration()
         
            print("\nRendering Sign:")
            render_sign_contents()
            
        
        else:
            print("Updating Sign Timestamp")
            save_configuration()
         
            print("\nRendering Sign:")
            render_sign_contents()
        
   
except Exception as e:
    print("Problem occurred in main program:", e)
    
