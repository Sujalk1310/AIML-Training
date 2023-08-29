import pip
import cv2
pip.main(['install', 'opencv-python'])
def sketch(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    canny_edges = cv2.Canny(img_gray_blur, 60, 70)
    _, mask = cv2.threshold(canny_edges, 200, 255, cv2.THRESH_BINARY_INV)
    return mask
cap = cv2.VideoCapture(0)
while True :
    ret, frame = cap.read()
    cv2.namedWindow("Live Sketcher", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Live Sketcher",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Live Sketcher',sketch(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()