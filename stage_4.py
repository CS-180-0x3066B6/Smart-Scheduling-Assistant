import pytesseract
import numpy as np
from Stage_5 import find_date
#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
imagedata = np.ndarray

def ocr(some_subimage : imagedata, current_date):
    print("*****************************************************")
    assert(current_date != None)
    text =pytesseract.image_to_string(some_subimage)
    assert(type(text)==str)
    print("Current Date: " + str(current_date))
    print("Text: " + text)
    found_dates = find_date(text, current_date)
    assert(type(found_dates) == list)
    print("Found Dates: " + str(found_dates))
    print("*****************************************************")
    assert(type(found_dates) == list)
    return found_dates, text
  
def ocr_test():  
    from PIL import Image
   # pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    filename = '001.tif'
    img1 = np.array(Image.open(filename))
    print(ocr(img1)) 

#ocr_test()
