import pytesseract
import numpy as np
from Stage_5 import find_date
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
imagedata = np.ndarray

def ocr(some_subimage : imagedata):
    text = pytesseract.image_to_string(some_subimage)
    found_dates = find_date(text)
    print(found_dates)
    return found_dates
  
def ocr_test():  
    from PIL import Image
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    filename = '001.tif'
    img1 = np.array(Image.open(filename))
    print(ocr(img1)) 


