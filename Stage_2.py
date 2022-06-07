from typing import Optional
import numpy
from stage_3 import bfs_selector
import datetime
imagedata = numpy.ndarray
path = str
class OCR_Node:
      def __init__(self,row_height:int = -1, row_number:int = -1):
          self.row_height = row_height
          self.row_number:int = row_number
          self.children: list[OCR_Node]= list()
          self.subimage: Optional[imagedata] = None
          self.is_dummy = True

def subdivide(size: int, some_image: imagedata)->OCR_Node:
    assert(type(size) == int);
    #assert(size >= 10);
    #assert(size <= 120);
    assert(type(some_image) == imagedata);
    assert(len(some_image) > 0)
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
        row_end = size*(x+1)
        if row_end >image_height -1:
            row_end = image_height -1
        new_node.subimage = some_image[x*size:row_end]
        new_node.is_dummy = False
        all_nodes.append(new_node)
    #Put nodes into a complete binary tree, rooted at top_node; Do this by copying references into each OCR_Node's children attribute
    #Note: row_number+1 is each node's
    if total_subimages > 1:
        top_node.children = [all_nodes[0],all_nodes[1]]
    else:
        top_node.children = [all_nodes[0]]
    for x in range(len(all_nodes)):
        lson_index  = (x+1)*2
        rson_index  = (x+1)*2+1
        if lson_index <= max_node_index:
            all_nodes[x].children.append(all_nodes[lson_index])
        if rson_index <= max_node_index:
            all_nodes[x].children.append(all_nodes[rson_index])
    assert(type(top_node) == OCR_Node)
    return top_node

# def bfs_selector(root_node: OCR_Node,img_path:path)->None:
#     pass

def image_divider(some_image: imagedata, img_path: path, current_date:  datetime.datetime, noprune: bool)-> None:
    assert(type(current_date) == datetime.datetime)
    assert(type(some_image) == imagedata)
    assert(type(img_path) == path)
    #image_height = len(some_image)
    sizes_tried: set[int] = set()
    tri_point = [30,80,130]
    twenties = [20,40,60,100,120]
    fine_sizes = [x for x in range(20,161,3)]
    ultrafine_sizes = [x for x in range(20,161)]
    settings = [tri_point,twenties,fine_sizes, ultrafine_sizes]
    for setting in settings:
        if setting is ultrafine_sizes:
            print("Tried using ultrafine on ",img_path)
        children: list[OCR_Node] = []
        for size in setting:
            if size not in sizes_tried:
                children.append(subdivide(size,some_image))
                sizes_tried.add(size)
        top_node = OCR_Node()
        top_node.children = children
        if bfs_selector(top_node,img_path,current_date, noprune) != 2:
            break
