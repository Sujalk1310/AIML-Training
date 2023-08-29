import cv2
WebCam = cv2.VideoCapture(0)
Trainer = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
while True :
    _ , Frame = WebCam.read()
    # Frame = cv2.flip(Frame,1)
    GFrame = cv2.cvtColor(Frame,cv2.COLOR_BGR2GRAY)
    # FaceCords = Trainer.detectMultiScale(GFrame,1.4,4)
    # for (x,y,w,h) in FaceCords:
    #     cv2.rectangle(Frame,(x,y),(x+w,y+h),(0,255,0),2)
    #     cv2.putText(Frame,"Human",(x,y-4),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),3)
    cv2.imshow("DCAM",Frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
WebCam.release()
cv2.destroyAllWindows()
