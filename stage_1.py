#imports
import os
from Stage_2 import image_divider
from turtle import clear
from IPython import display
from typing import Optional
import numpy
import datetime
import cv2
import os
import shutil
import sys
path=str
imagedata=numpy.ndarray

current_date:datetime.datetime=None

def reset_data():
    path1="60"
    if os.path.isdir(path1):
        shutil.rmtree(path1)
    if os.path.isfile("data.json"):
        os.remove("data.json")

class OCR_Node:
    def __init__(self,row_height:int = -1, row_number:int = -1):
        self.row_height = row_height 
        self.row_number:int = row_number 
        self.children: list[OCR_Node]= list() 
        self.subimage: Optional[imagedata] = None
        self.is_dummy = True 

    #end of testing
def str_to_datetime(date_string: str)->datetime.datetime:
    if len(date_string)==10:
        m,d,y=date_string.split('-')
        return datetime.datetime(int(y),int(m),int(d))
    elif len(date_string)==7:
        m,y=date_string.split('-')
        return datetime.datetime(int(y),int(m),1)
    elif len(date_string)==4:
        return datetime.datetime(int(date_string),1,1)
#start of stage 1
def import_data(datapath:path,noprune:bool=False)->None:
    print(noprune)
    global current_date
    count=0
    reset_data()
    for file in os.listdir(datapath):
        print("--------------------------------------------------------------------------------")
        if count==10:
            break
        if file.endswith(".tif"):
            print("FILENAME: " + file)
            current_date_file=open("current_date.txt",'r')
            date_lines=current_date_file.readlines()
            for date_line in date_lines:
                fname,current_str_date=date_line[:-1].split(' ')
                if fname==file:
                    current_date=str_to_datetime(current_str_date)
                    break
            current_date_file.close()
            full_directory=datapath+file
            imgdata:imagedata=cv2.imread(full_directory)
            assert(current_date != None)
            image_divider(imgdata,full_directory,current_date,noprune)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        count+=1
        
if __name__=="__main__":
    print("starting")
    args=str(sys.argv)
    if "noprune" in args:
        import_data("Learning/Sample/",True) #path
    else:
        import_data("Learning/Sample/")
