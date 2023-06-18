import pip
import cv2
import numpy as np

pip.main(['install', 'opencv-python'])

def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)

def imgtosketch(img, k_size):
    grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert Image
    invert_img=cv2.bitwise_not(grey_img)
    #invert_img=255-grey_img

    # Blur image
    blur_img=cv2.GaussianBlur(invert_img, (k_size,k_size),0)

    # Invert Blurred Image
    invblur_img=cv2.bitwise_not(blur_img)
    #invblur_img=255-blur_img

    # Sketch Image
    sketch_img=cv2.divide(grey_img,invblur_img, scale=256.0)
    return sketch_img
cap = cv2.VideoCapture(0)
while True :
    ret, frame = cap.read()
    w = int(cap.get(3))
    h = int(cap.get(4))
    # frame = cv2.flip(frame, 1) # flip
    frame = frame[:, 0+200 : 200+350]
    sketch = imgtosketch(frame, 111) # twitch sketch
    sketch = gammaCorrection(sketch, 0.5) # twitch gamma
    cv2.rectangle(sketch,(0,0),(w,30),(0,0,0),-1)
    cv2.rectangle(sketch,(0,h-35),(w,h),(0,0,0),-1)
    cv2.rectangle(sketch,(0,0),(10,h),(0,0,0),-1)
    cv2.rectangle(sketch,(340,0),(w,h),(0,0,0),-1)
    cv2.putText(sketch, "AI Generated Sketch", (88, 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(sketch, "Created by DedSec", (95, h-13), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow('Live Sketcher', sketch)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('sketch.png', sketch)
        break
cap.release()
cv2.destroyAllWindows()