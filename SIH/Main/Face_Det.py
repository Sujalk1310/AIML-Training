import cv2

webcam=cv2.VideoCapture(0)
trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    _ ,frame = webcam.read()
    frame = cv2.flip(frame, 1)
    grayscaled_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_coordinates = trained_face_data.detectMultiScale(grayscaled_frame)
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,25)
    fontScale              = 0.5
    fontColor              = (255,255,255)
    thickness              = 2
    lineType               = 2
    # For detecting multiple faces !!
    # for i in face_coordinates:
    #     (x, y, h, w) = i
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    try:
        (x, y, h, w) = face_coordinates[0]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    except:
        cv2.putText(frame,'No Face Detected !!', 
                bottomLeftCornerOfText, 
                
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)
    cv2.imshow("CAM",frame)
    if cv2.waitKey(2) & 0xff ==ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()