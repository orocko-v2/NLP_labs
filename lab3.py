from PIL import Image

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Users/HELLO/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'

def read_Images():
    list = []
    img1 = Image.open('data/scans/medieval_page_1.jpeg')
    img2 = Image.open('data/scans/medieval_page_2.jpeg')
    img3 = Image.open('data/scans/medieval_page_3.jpeg')
    img4 = Image.open('data/scans/medieval_page_4.jpeg')
    list.append(img1)
    list.append(img2)
    list.append(img3)
    list.append(img4)
    return list

def image_to_String(image):
    return pytesseract.image_to_string(image)

list = []
for i in read_Images():
    list.append(image_to_String(i))

print(list[0])


