import cv2
import imutils
import numpy as np
import save
import re
import easyocr


reader = easyocr.Reader(['en'])

def is_valid_plate(plate):
    """Check if the plate matches standard Indian number plate formats."""
    patterns = [
        r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}$",  # Normal Plate (MH12AB1234)
        r"^[0-9]{2}BH[0-9]{4}[A-Z]{1,2}$",          # BH Series (21BH1234Z)
        r"^DL[0-9]{1,2}C[A-Z]{1,2}[0-9]{4}$",  
        r"^DL[ ]?[0-9]{1,2}[A-Z]{2}[ ]?[0-9]{4}$"
      
    ]
    for pattern in patterns:
        if re.match(pattern, plate):
            return True
    return False

def rec(img):
    """Detect number plate and extract text."""
    img = cv2.resize(img, (640, 480)) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe=cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray=clahe.apply(gray)

    cascade = cv2.CascadeClassifier("C:/Users/hp/Downloads/haarcascade_russian_plate_number.xml")
    nplate = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 30))

    for (x, y, w, h) in nplate:
        plate = img[y:y+h, x:x+w] 
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)  #Green Box

        gray_plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        _, plate = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        text = reader.readtext(plate)
        if text:
            plate_text = text[0][1].replace(" ", "").upper()
            if is_valid_plate(plate_text):
              
                save.write(plate_text)
            '''else:
                print(f"Invalid Plate Detected: {plate_text}")'''

        break 

    return img

