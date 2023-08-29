import cv2
import pytesseract
import pyttsx3
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
Cam = cv2.VideoCapture(0)
while 1:
    _ , img = Cam.read()
    Fimg = img
    cv2.imshow('CAM',img)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    waste, img_bin = cv2.threshold(img,100,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img = cv2.bitwise_not(img_bin)
    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    cong = r'-l eng --oem 1 --psm 4 --tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
    boxes = pytesseract.image_to_data(img,config=cong)
    Text = ""
    for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b)==12:
                x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                cv2.rectangle(Fimg,(x,y),(w+x,h+y),(0,0,255),3)
                cv2.putText(Fimg,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
                Text = b[11]+' '
                print(Text)
                engine = pyttsx3.init()
                engine.say(Text) 
                engine.runAndWait()
                cv2.imwrite("Image.jpg",Fimg)
                cv2.imwrite("ImageDet.jpg",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
Cam.release()
cv2.destroyAllWindows()

