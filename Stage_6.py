import json
import os
import datetime
from typing import Optional
import cv2


# Data to be written
def output_summary(parsed_dates:dict, img_path:str, text):


    # Create a list of items to convert to JSON
    json_list = []

    # Iterate through the parsed_dates dictionary
    for date,value in parsed_dates.items():
        for event in value:
            print(date,event)
        # Create a dictionary of the parsed_dates
            json_dict = {}
            json_dict['date'] = date
            json_dict['path'] = img_path
            json_dict['text'] = text[date]
        
            splits = img_path.split("/")
            origfilename = splits[-1][:-4]
            r_height = str(event.row_height)
            r_number = str(event.row_number)
            subimg = event.subimage

            pathlist = ["smart_assistant", "image_segments"]
            pathlist.append(origfilename)
            pathlist.append(r_height)
        
            sbimg = ""
            for i in range(len(pathlist)):
                 sbimg = sbimg + pathlist[i] + "/"
        
                 sbpth = sbimg
                 sbpth = sbpth + r_number + ".png"
            json_dict['subimage_path'] = sbpth
        
            owd = os.getcwd()
            for i in range(len(pathlist)):
                if(os.path.exists(pathlist[i]) == True ):
                    os.chdir(pathlist[i])
                else:
                    os.mkdir(pathlist[i])
                    os.chdir(pathlist[i])
            cv2.imwrite(r_number+".png", subimg)    
            os.chdir(owd)       
        
        # Add the dictionary to the list if date is not in the past
        # if datetime.datetime.strptime(date, "%m %d %Y") > currentDate:
            json_list.append(json_dict)

    # Check if file exists, create new if no, append if yes
    if not os.path.isfile('data.json'):
        json_create(json_list)
    else:
        for item in json_list:
            json_append(item)


# Function to add to existing JSON
def json_append(data, jsonfile='data.json'):
    master = {}

    # Opening JSON file
    with open(jsonfile, 'r') as file:
        master = json.load(file)
    # Append the data to the JSON file
    master.append(data)
    # Write the data to a file
    with open(jsonfile, 'w') as file:
        json.dump(master, file, indent = 4)


# Function to create a Json file
def json_create(master, jsonfile='data.json'):
    with open(jsonfile, 'w') as file:
        json.dump(master, file, indent = 4)

