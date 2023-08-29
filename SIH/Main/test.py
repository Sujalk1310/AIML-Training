import cv2 
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
kernel = np.ones((2, 1), np.uint8)
Fimg = cv2.imread("test.png")
img = Fimg
img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
img = cv2.erode(img, kernel, iterations=1) 
img = cv2.dilate(img, kernel, iterations=1)
cong = r'-l eng --oem 1 --psm 4'
boxes = pytesseract.image_to_data(img,config=cong)
Text = ""
for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b)==12:
                x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                cv2.rectangle(Fimg,(x,y),(w+x+y),(0,0,255),3)
                cv2.putText(Fimg,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
                Text = b[11]+' '
                print(Text)
                cv2.imwrite("Image.jpg",Fimg)
                cv2.imwrite("ImageDet.jpg",img)
