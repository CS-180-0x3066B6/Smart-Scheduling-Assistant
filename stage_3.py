from cgitb import small
# import os
# from subprocess import NORMAL_PRIORITY_CLASS
# from PIL import Image
# from IPython import display
from typing import Optional
import numpy
path=str
imagedata=numpy.ndarray
from stage_4 import ocr
from Stage_6 import output_summary
import datetime

def str_to_datetime(date_string:str)-> datetime.datetime:
    if len(date_string)==10:
        m,d,y=date_string.split('-')
        return datetime.datetime(int(y),int(m),int(d))
    elif len(date_string)==7:
        m,y=date_string.split('-')
        return datetime.datetime(int(y),int(m),1)
    elif len(date_string)==4:
        return datetime.datetime(int(date_string),1,1)
class OCR_Node:
    def __init__(self,row_height:int = -1, row_number:int = -1):
        self.row_height = row_height 
        self.row_number:int = row_number 
        self.children: list[OCR_Node]= list() 
        self.subimage: Optional[imagedata] = None
        self.is_dummy = True 

#start of stage 3
def bfs_selector(root_node: OCR_Node, img_path: path,current_date:datetime.datetime,noprune:bool)->None:
    newer_detected=False
    queue:list[OCR_Node]=[]
    dates:dict[int,dict[str,list[OCR_Node]]]={}
    smallest_row=121
    for child in root_node.children:#appending initial children 
        queue.append(child)
    while len(queue)>0:
        current_node=queue.pop(0)
        if current_node.row_height<=smallest_row:
            result=[]
            if not current_node.is_dummy:  
                result:list[str]=ocr(current_node.subimage, current_date)
            for date in result:
                temp_date:datetime.datetime=str_to_datetime(date)
                if temp_date>current_date:
                    if not newer_detected:
                        newer_detected=True
                        dates={}
                    smallest_row=current_node.row_height
                    if current_node.row_height not in dates:
                        dates[current_node.row_height]={}
                    if date not in dates[current_node.row_height]:
                        dates[current_node.row_height][date]=[]
                    dates[current_node.row_height][date].append(current_node)
                else:
                    if not newer_detected:
                        if current_node.row_height not in dates:
                            dates[current_node.row_height]={}
                        if date not in dates[current_node.row_height]:
                            dates[current_node.row_height][date]=[]
                        dates[current_node.row_height][date].append(current_node)#past nodes
            for child in current_node.children: #append all child to queue
                queue.append(child)
    if noprune:
        for value in dates.values():
            output_summary(value,img_path)
    else:
        smallest_dates:dict[str,list[OCR_Node]]={}
        if smallest_row!=121:
            smallest_dates=dates[smallest_row]#there exists dates in the image file
        print("Displaying output-",smallest_row)
        print(smallest_dates)
        output_summary(smallest_dates,img_path)
