import cv2 
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


webcam=cv2.VideoCapture(0)

font_scale=3
font=cv2.FONT_HERSHEY_PLAIN

while True:
    frame=cv2.imread('Car.jpg')
   
    ClassIndex,confidece,bbox=model.detect(frame,confThreshold=0.60)


    if (len(ClassIndex)!=0):
        for ClassInd,conf,boxes in zip(ClassIndex.flatten(),confidece.flatten(),bbox):
            if (ClassInd<=80):
                cv2.rectangle(frame,boxes,(255,0,0),2)
  
    for (x,y,w,h) in bbox:
        if (w*h)>=215000:
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
            if ClassInd < 81 :
                text = classLabels[ClassInd-1]+ ' ' + str('%.2f' % conf) + '%'
                cv2.putText(frame,text,(x+10,y-20),font,fontScale=1,color = (255,0,0))
    cv2.imshow("CAM",frame)
    cv2.imwrite("Test.jpg",frame)
            

        
    if cv2.waitKey(2) & 0xff ==ord('q'):
        break
webcam.release()
cv2.destroyAllWindows()

