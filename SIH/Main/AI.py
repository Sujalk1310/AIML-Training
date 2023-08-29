import cv2 
import pytesseract
import pyttsx3
import numpy as np

Cond = 0
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
kernel = np.ones((2, 1), np.uint8)
webcam=cv2.VideoCapture(0)
Speak = ""
CSP = ""
def OCR(img):
    # OCR !!
    print("OCR Opened")
    Fimg = img
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    img = cv2.erode(img, kernel, iterations=1) 
    img = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite("Test.png",img)
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

# Object Detection !! 
frozen_model=r'frozen_inference_graph.pb'
config_file=r'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
model = cv2.dnn_DetectionModel(frozen_model,config_file)
classLabels=[]
file_name='labels.txt'
with open(file_name,'rt') as f:
    classLabels=f.read().rstrip('\n').split('\n')
model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5,127.5,127.5))
model.setInputSwapRB(True)
font_scale=3
font=cv2.FONT_HERSHEY_PLAIN

# Running OCR !!

while True:
    kuccho,frame=webcam.read()
    if (Cond == 30): # Button Press Condition !!
        img = frame
        OCR(img)
        Cond = 0
    else :
        Cond += 1
    ClassIndex,confidece,bbox=model.detect(frame,confThreshold=0.60)


    if (len(ClassIndex)!=0):
        for ClassInd,conf,boxes in zip(ClassIndex.flatten(),confidece.flatten(),bbox):
            if(ClassInd<=80):
                cv2.rectangle(frame,boxes,(255,0,0),2)
  
    for (x,y,w,h) in bbox:
        if (w*h)>=260000:
            font                   = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10,50)
            fontScale              = 1
            fontColor              = (255,255,255)
            thickness              = 5
            lineType               = 2

            cv2.putText(frame,'Something in front!', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)
            engine = pyttsx3.init()
            engine.say("Something in Front")
            engine.say("please wait") 
            engine.runAndWait()
        if ClassInd < 81 :
            text = classLabels[ClassInd-1]+ ' ' + str('%.2f' % conf) + '%'
            cv2.putText(frame,text,(x+10,y+20),font,fontScale=1,color = (255,0,0))
            Speak = classLabels[ClassInd-1]
            if Speak != CSP and Cond == 15:
                engine = pyttsx3.init()
                engine.say(Speak)
                engine.runAndWait()
                CSP = Speak
    cv2.imshow("CAM",frame)
            

        
    if cv2.waitKey(2) & 0xff ==ord('q'):
        break
webcam.release()
cv2.destroyAllWindows()

