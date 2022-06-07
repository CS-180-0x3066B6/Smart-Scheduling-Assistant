from cgitb import small
from hmac import new
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
def bfs_selector(root_node: OCR_Node, img_path: path,current_date:datetime.datetime,noprune:bool)->int:
    newer_detected=False
    current_date_found=False
    queue:list[OCR_Node]=[]
    dates:dict[int,dict[str,list[OCR_Node]]]={}
    texts : dict[int,dict[str,list[OCR_Node]]]={}
    smallest_row=121
    for child in root_node.children:#appending initial children 
        queue.append(child)
    while len(queue)>0:
        current_node=queue.pop(0)
        if current_node.row_height<=smallest_row:
            result=[]
            if not current_node.is_dummy:  
                result, text = ocr(current_node.subimage, current_date)
                print(result)
            for date in result:
                print("found date in =>",date,current_node.subimage)
                temp_date:datetime.datetime=str_to_datetime(date)
                if temp_date>current_date:
                    if not newer_detected:
                        newer_detected=True
                        dates={}
                        texts={}
                    smallest_row=current_node.row_height
                    if current_node.row_height not in dates:
                        dates[current_node.row_height]={}
                        texts[current_node.row_height]={}
                    if date not in dates[current_node.row_height]:
                        dates[current_node.row_height][date]=[]
                        texts[current_node.row_height][date]=[]
                    dates[current_node.row_height][date].append(current_node)
                    texts[current_node.row_height][date].append(text)
                else:
                    if not newer_detected:
                        current_date_found=True
                        if current_node.row_height not in dates:
                            dates[current_node.row_height]={}
                            texts[current_node.row_height]={}
                        if date not in dates[current_node.row_height]:
                            dates[current_node.row_height][date]=[]
                            texts[current_node.row_height][date]=[]
                        dates[current_node.row_height][date].append(current_node)#past nodes
                        texts[current_node.row_height][date].append(text)
            for child in current_node.children: #append all child to queue
                queue.append(child)
    if noprune:
        for key, value in dates.items():
            output_summary(value,img_path,texts[key])
    else:
        smallest_dates:dict[str,list[OCR_Node]]={}
        smallest_dates_text : dict[int,dict[str,list[OCR_Node]]]={}
        if smallest_row!=121:
            smallest_dates=dates[smallest_row]#there exists dates in the image file
            smallest_dates_text = texts[smallest_row]
        else:
            if not current_date_found:
                return 2
        print("Displaying output->",smallest_row,smallest_dates)
        for key, value in smallest_dates.items():
            print(value[0].row_height,value[0].row_number)
        output_summary(smallest_dates,img_path,smallest_dates_text)
    if newer_detected:
        return 0
    return 1
