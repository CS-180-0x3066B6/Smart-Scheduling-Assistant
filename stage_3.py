from cgitb import small
import os
from PIL import Image
from IPython import display
from typing import Optional
import numpy
path=str
imagedata=numpy.ndarray
from stage_1 import str_to_datetime
from stage_4 import ocr
from Stage_6 import output_summary
import datetime
current_date=None
class OCR_Node:
    def __init__(self,row_height:int = -1, row_number:int = -1):
        self.row_height = row_height 
        self.row_number:int = row_number 
        self.children: list[OCR_Node]= list() 
        self.subimage: Optional[imagedata] = None
        self.is_dummy = True 

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
                print(result)
            for date in result:
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