#imports
import os
from PIL import Image
from IPython import display
from typing import Optional
import numpy
import datetime
from Stage_2 import OCR_Node, image_divider


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

def subdivide(size: int, some_image: imagedata)->OCR_Node:
    image_height = len(some_image)
    total_subimages = int(image_height/size)
    if image_height % size > 0:
        total_subimages += 1
    top_node = OCR_Node(row_height=size)
    all_nodes: list[OCR_Node] = list()
    max_node_index = len(all_nodes) - 1
    #Decompose some_image into indexed OCR_Nodes
    for x in range(total_subimages):
        new_node = OCR_Node(row_height = size,row_number = x)
        row_end = x*(size+1)
        if row_end >image_height -1:
            row_end = image_height -1
        new_node.subimage = some_image[:][x*size:row_end]
        new_node.is_dummy = False
        all_nodes.append(new_node)
    #Put nodes into a complete binary tree, rooted at top_node; Do this by copying references into each OCR_Node's children attribute
    #Note: row_number+1 is each node's
    if total_subimages > 1:
        top_node.children = [all_nodes[0],all_nodes[1]]
    else:
        top_node.children = [all_nodes[0]]
    for x in range(len(all_nodes)):
        lson_index  = (x+1)*2+1
        rson_index  = (x+1)*2+2
        if lson_index <= max_node_index:
            all_nodes[x].children.append(all_nodes[lson_index])
        if rson_index <= max_node_index:
            all_nodes[x].children.append(all_nodes[rson_index])
    return top_node




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
    for file in os.listdir(datapath):
        if file.endswith(".tif"):
            current_date_file=open("current_date.txt",'r')
            date_lines=current_date_file.readlines()
            for date_line in date_lines:
                fname,current_str_date=date_line[:-1].split(' ')
                # print(fname,file)
                if fname==file:
                    current_date=str_to_datetime(current_str_date)
            full_directory=datapath+file
            print(current_date)
            img=Image.open(full_directory)
            imgdata=numpy.array(img)
            image_divider(imgdata,full_directory)

import_data("Learning/") #path
