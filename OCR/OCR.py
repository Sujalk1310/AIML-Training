import cv2
import pytesseract
import pyttsx3
import numpy as np

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Initialize camera
Cam = cv2.VideoCapture(0)

# Define kernel for image processing
kernel = np.ones((2, 1), np.uint8)

while True:
    ret, img = Cam.read()
    
    if not ret:
        break
    
    # Make a copy of the original image for drawing rectangles and text
    Fimg = img.copy()
    
    # Convert image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Reduce glare using adaptive thresholding
    th_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
    
    # Apply morphological operations to enhance text detection
    img = cv2.erode(th_img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    
    # Perform OCR on the processed image
    cong = r'-l eng --oem 1 --psm 4 --tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
    boxes = pytesseract.image_to_data(img, config=cong, output_type=pytesseract.Output.DICT)
    
    for i in range(len(boxes['text'])):
        x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
        confidence = int(boxes['conf'][i])
        text = boxes['text'][i].strip()  # Remove leading/trailing whitespace
        
        if confidence > 50 and text:  # Avoid blank messages and low confidence
            x, y, w, h = int(x), int(y), int(w), int(h)  # Convert to integers
            
            # Draw rectangle and text
            cv2.rectangle(Fimg, (x, y), (x + w, y + h), (0, 0, 255), 3)
            print(text)
            cv2.putText(Fimg, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
            
            # Initialize text-to-speech engine
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
    
    # Display the processed image with text and rectangles
    cv2.imshow('Text Detection', Fimg)
    
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
Cam.release()
cv2.destroyAllWindows()
