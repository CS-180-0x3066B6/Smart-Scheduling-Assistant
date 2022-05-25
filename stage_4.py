import pytesseract
import numpy as np
from Stage_5 import find_date
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
imagedata = np.ndarray

def ocr(some_subimage : imagedata):
    print(type(some_subimage))
    text = pytesseract.image_to_string(some_subimage)
    print(text)
    found_dates = find_date(text)
    return found_dates
  
def ocr_test():  
    from PIL import Image
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    filename = '001.tif'
    img1 = np.array(Image.open(filename))
    print(ocr(img1)) 

ocr_test()
