import cv2, os, numpy as np
from PIL import Image
def getImagesAndLabels(path):
    ImgPath = [os.path.join(path,i) for i in os.listdir(path)]
    FSamples = []
    FIds = []
    for i in ImgPath:
        TrainedImg = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        Gi = Image.open(i).convert('L')
        Numi = np.array(Gi,'uint8')
        Id = int(os.path.split(i)[-1].split(".")[1])
        Faces = TrainedImg.detectMultiScale(Numi)
        for (x,y,w,h) in Faces:
            FSamples.append(Numi[y:y+h,x:x+w])
            FIds.append(Id)
    return FSamples,FIds
def Trainer():
    WebCam = cv2.VideoCapture(0)
    TrainedImg = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    Name = input("Enter Face Name : ")
    Id = input("Enter Face ID : ")
    N = 0
    while True :
        _ , FrameRaw = WebCam.read()
        Frame = cv2.flip(FrameRaw,1)
        GFrame = cv2.cvtColor(Frame,cv2.COLOR_BGR2GRAY)
        FaceCord = TrainedImg.detectMultiScale(GFrame,1.4,4)
        for (x,y,w,h) in FaceCord :
            cv2.rectangle(Frame,(x,y),(x+w,y+h),(0,255,0),2)
            N += 1
            cv2.imwrite("DataSet/"+Name+"."+Id+"."+str(N)+".png",GFrame[y:y+h,x:x+w])
            cv2.imshow('Saving in progress...',Frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif N > 200 :
            print("Image Saved Successfully !!")
            break
    Rec = cv2.face.LBPHFaceRecognizer_create()
    FaceName,ID = getImagesAndLabels("DataSet")
    Rec.train(FaceName,np.array(ID))
    Rec.save("Model/Trained_Faces.yml")
    print("Model Trained !!")
    WebCam.release()
    cv2.destroyAllWindows()
def Recognizer():
    Rec = cv2.face.LBPHFaceRecognizer_create()
    Rec.read("Model/Trained_Faces.yml")
    TrainedImg = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    WebCam = cv2.VideoCapture(0)
    while True :
        _ , FrameRaw = WebCam.read()
        Frame = cv2.flip(FrameRaw,1)
        GFrame = cv2.cvtColor(Frame,cv2.COLOR_BGR2GRAY)
        FaceCord = TrainedImg.detectMultiScale(GFrame,1.4,6)
        for (x,y,w,h) in FaceCord :
            ID , Conf = Rec.predict(GFrame[y:y+h,x:x+w])
            Conf = 100*(1-(Conf/300))
            cv2.rectangle(Frame,(x,y),(x+w,y+h),(0,255,0),2)
            if int(Conf) >= 65:    
                cv2.putText(Frame,f"{str(ID)},{int(Conf)}%",(x,y-4),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),3)
        cv2.imshow('Face Recognition',Frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    WebCam.release()
    cv2.destroyAllWindows()
while True :
    for i in range (3):
        print("")
    print("What do you want to do ? (1-3) :")
    print("1. Train Face")
    print("2. Recognize Face")
    print("3. Exit")
    n = int(input())
    if n == 1:
        Trainer()
    elif n == 2:
        Recognizer()
    elif n == 3:
        print("!! Thank You !!")
        break
    else :
        print("!! Invalid Input !!")