from cgitb import small
import os
from PIL import Image
from IPython import display
from typing import Optional
import numpy
import datetime
from Stage_6 import output_summary
from stage_4 import ocr


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


def str_to_datetime(date_string):
    if len(date_string)==10:
        m,d,y=date_string.split('-')
        return datetime.datetime(int(y),int(m),int(d))
    elif len(date_string)==7:
        m,y=date_string.split('-')
        return datetime.datetime(int(y),int(m),1)
    elif len(date_string)==4:
        return datetime.datetime(int(date_string),1,1)

#dummy stage 4
# def ocr(some_subimage: imagedata)-> list[str]:
#     found_date=None
#     date_type=None
#     return []

#dummy stage 6
# def output_summary(parsed_dates:dict[str,OCR_Node], img_path:path, root_node: OCR_Node)->None:
#     pass

#start of stage 3
def bfs_selector(root_node: OCR_Node, img_path: path):
    newer_detected=False
    queue:list[OCR_Node]=[]
    dates:dict[int,dict[str,OCR_Node]]={20:{},40:{},60:{},80:{},100:{},120:{}}
    smallest_row=121
    for child in root_node.children:#appending initial children
        queue.append(child)
    while len(queue)>0:
        current_node=queue.pop(0)
        if current_node.row_height<=smallest_row:
            result=[]
            if not current_node.is_dummy:  
                result=ocr(current_node.subimage)
            for date in result:
                print(result)
                temp_date=str_to_datetime(date)
                if temp_date>current_date:
                    if not newer_detected:
                        newer_detected=True
                        dates={20:{},40:{},60:{},80:{},100:{},120:{}}
                    smallest_row=current_node.row_height
                    dates[current_node.row_height][date]=current_node
                else:
                    if not newer_detected:
                        dates[current_node.row_height][date]=current_node #past nodes
            for child in current_node.children: #append all child to queue
                queue.append(child)
    smallest_dates=None
    if smallest_row!=121:
        smallest_dates=dates[smallest_row]#there exists dates in the image file
    output_summary(smallest_dates,img_path)