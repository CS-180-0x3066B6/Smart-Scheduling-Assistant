#imports
import os
from turtle import clear
from PIL import Image
from IPython import display
from typing import Optional
import numpy
import datetime
from Stage_2 import OCR_Node, image_divider
import cv2

path=str
imagedata=numpy.ndarray
current_date=None
class OCR_Node:
    def __init__(self,row_height:int = -1, row_number:int = -1):
        self.row_height = row_height 
        self.row_number:int = row_number 
        self.children: list[OCR_Node]= list() 
        self.subimage: Optional[imagedata] = None
        self.is_dummy = True 

    #end of testing
def str_to_datetime(date_string):
    if len(date_string)==10:
        m,d,y=date_string.split('-')
        return datetime.datetime(int(y),int(m),int(d))
    elif len(date_string)==7:
        m,y=date_string.split('-')
        return datetime.datetime(int(y),int(m),1)
    elif len(date_string)==4:
        return datetime.datetime(int(date_string),1,1)
#start of stage 1
def import_data(datapath:path)->None:
    global current_date
    count=0
    for file in os.listdir(datapath):
        if count==10:
            break
        if file.endswith(".tif"):
            current_date_file=open("current_date.txt",'r')
            date_lines=current_date_file.readlines()
            for date_line in date_lines:
                fname,current_str_date=date_line[:-1].split(' ')
                # print(fname,file)
                if fname==file:
                    current_date=str_to_datetime(current_str_date)
            full_directory=datapath+file
            imgdata=cv2.imread(full_directory)
            image_divider(imgdata,full_directory)
        count+=1

import_data("Learning/") #path
