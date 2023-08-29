import cv2
import pytesseract
import pyttsx3
import numpy as np
import os

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Define kernel for image processing
kernel = np.ones((2, 1), np.uint8)

# Loading the test image
img = cv2.imread("test.jpg")

img = cv2.flip(img, 1)
Fimg = img.copy()

# Convert image to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Reduce glare using adaptive thresholding
# th_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
    
# Apply morphological operations to enhance text detection
img = cv2.erode(gray_img, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
   
# Perform OCR on the processed image
cong = r'-l eng --oem 1 --psm 4 --tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
boxes = pytesseract.image_to_data(img, config=cong, output_type=pytesseract.Output.DICT)
text = ""

for i in range(len(boxes['text'])):
    confidence = int(boxes['conf'][i])
    text += " " + boxes['text'][i].strip()  # Remove leading/trailing whitespace

    if confidence > 50 and text:  # Avoid blank messages and low confidence
        print(boxes['text'][i].strip())

cv2.putText(Fimg, text, (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
cv2.imshow('Text Detection', Fimg)
cv2.waitKey(0)  # Wait for any key press
cv2.destroyAllWindows()
