import numpy as np
from keras.models import load_model
import cv2

def PreviewPane(w, Frame, result):
    Frame = cv2.rectangle(Frame, (0, 0), (w, 60), (255, 255, 255), -1)
    font                   = cv2.FONT_HERSHEY_DUPLEX
    bottomLeftCornerOfText = (10, 50)
    fontScale              = 1
    fontColor              = (0, 0, 0)
    thickness              = 1
    lineType               = 2
    text                   = f"Opt1 - {result[0][0] * 100 : .2f}    ||  Opt2 - {result[0][1] * 100 : .2f}"
    Frame = cv2.putText(
        Frame, 
        text, 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        thickness,
        lineType,
    )
    cv2.imshow("Preview Pane", Frame)

def PredDisp(model):
    print()
    print("Loading Preview Pane...")
    print()
    Webcam = cv2.VideoCapture(0)
    print("Press 'q' anytime to exit preview pane...")
    print()
    while True:
        _, RawImg = Webcam.read()
        Frame = cv2.flip(RawImg, 1)
        PredFrame = cv2.resize(Frame, (64, 64))
        test_image = np.expand_dims(PredFrame, axis = 0)
        result = model.predict(test_image, verbose = 0)
        w = int(Webcam.get(3))
        PreviewPane(w, Frame, result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            Webcam.release()
            break

def RunModel():
    print("Loading the model...")
    model = load_model('model.h5')
    print()
    print("Model Loaded...")
    PredDisp(model)
