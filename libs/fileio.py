# -------------------------------------------
# File IO Library
# -------------------------------------------

import os
import time
import stat
import json
import shutil

# The Default location of the Data Directory
data_dir = "/home/pi/Desktop/iotcapstone_data"


# -------------------------------------------
# get_filename
# Returns the fully qualified filename
# -------------------------------------------
def get_filename(filename):
    if (data_dir not in filename):
        return data_dir + "/" + filename
    else:
        return filename


# -------------------------------------------
# get_data_directory
# Returns the directory where files are stored
# -------------------------------------------
def get_data_directory():
    return data_dir


# -------------------------------------------
# get_file_contents_as_string
# Returns the string contents of a data file
# OR None if nothing was found
# -------------------------------------------
def get_file_contents_as_string(filename):
    # Gets the Fully Qualified File Path 
    file_path = get_filename(filename)
        
    if not os.path.isfile(file_path):
        return None
    else:
        f = open(file_path, 'r')
        return str(f.read()) 


# -------------------------------------------
# get_file_contents_as_string
# Returns the string contents of a data file
# OR None if nothing was found
# -------------------------------------------
def get_file_contents_as_json(filename):
    # Gets the Fully Qualified File Path 
    file_path = get_filename(filename)
        
    if not os.path.isfile(file_path):
        return None
    else:
        f = open(file_path, 'r')
        string_contents = str(f.read())
        return json.loads(string_contents)
    

# -------------------------------------------
# get_time_since_last_modified
# Returns the amount of time (in seconds) since
# the file (or -1 if there is an error)
# -------------------------------------------
def get_time_since_last_modified(filename):
    # Gets the Fully Qualified File Path 
    file_path = get_filename(filename)
    
    # Returns a -1 if the file does not exist
    if not os.path.isfile(file_path):
        print("File", filename, "does not exist")
        return -1
    
    return round(float(time.time() - os.stat(file_path)[stat.ST_MTIME]), 1)


# -------------------------------------------
# write_file_contents
# Writes a string to a file
# -------------------------------------------
def write_to_file(filename, contents, mode='w'):
    # Gets the Fully Qualified File Path 
    file_path = get_filename(filename)
    
    # Writing to the File
    f = open(file_path, mode)
    f.write(contents)
    f.close()


# -------------------------------------------
# create_folder
# Creates a folder if it does not already exist
# -------------------------------------------
def create_folder(folder):
    folder_path = get_filename(folder)
    if not os.path.isdir(folder_path) and not os.path.isfile(folder_path):
        os.mkdir(folder_path)
        print("Folder", folder_path, "Created")


# -------------------------------------------
# file_exists
# Returns true if a file exists, and false otherwise
# -------------------------------------------
def file_exists(path):
    return os.path.isfile(path)


# -------------------------------------------
# copy_file
# -------------------------------------------
def copy_file(source_path, destination_path):
    try:
        shutil.copyfile(source_path, destination_path)
    except Exception as e:
        print("Problem Copying File:", e)
        

# -------------------------------------------
# Main
# This creates the data folder if it doesn't exist
# -------------------------------------------
create_folder(data_dir)
