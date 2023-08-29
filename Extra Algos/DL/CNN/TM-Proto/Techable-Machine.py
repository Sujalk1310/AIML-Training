import cv2
import os
import keyboard
import sys
from time import sleep
import Model_Trainer
import Run_Model

def TestOpt(Option_No):
    no_of_img = 0
    print("Taking Testing Data - 100")
    sleep(2)
    while True:
        _, RawImg = Webcam.read()
        Frame = cv2.flip(RawImg, 1)
        no_of_img += 1
        cv2.imshow("Capturing Opt" + str(Option_No) + "...", Frame)
        cv2.imwrite("dataset/Testing/Opt" + str(Option_No) + "/img" + str(no_of_img) + ".png", Frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif no_of_img > 99 :
            print("Testing Dataset Images for Opt" + str(Option_No) + " Saved Successfully !!")
            for i in range(3):
                print()
            cv2.destroyAllWindows()
            Webcam.release()
            break

def CaptOpt(Option_No):
    no_of_img = 0
    print("Taking Training Data - 200")
    sleep(2)
    while True:
        _, RawImg = Webcam.read()
        Frame = cv2.flip(RawImg, 1)
        no_of_img += 1
        cv2.imshow("Capturing Opt" + str(Option_No) + "...", Frame)
        cv2.imwrite("dataset/Training/Opt" + str(Option_No) + "/img" + str(no_of_img) + ".png", Frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif no_of_img > 199 :
            print("Training Dataset Images for Opt" + str(Option_No) + " Saved Successfully !!")
            for i in range(3):
                print()
            TestOpt(Option_No)
            break

# Menu (Console)
print()
print("Starting up Teachable Machine...")
sleep(2)
print()
print("Teachable Machine V1.0 - DedSec")
sleep(3)
while True:
    for i in range(3):
        print()
    print("Enter your preference: ")
    print("1. Opt1 Dataset Capturing")
    print("2. Opt2 Dataset Capturing")
    print("3. Train Deep Learning Model")
    print("4. Model Interface")
    print("5. Exit")
    print()
    key = keyboard.read_key()
    if (key in ['1', '2', '3', '4', '5']):
        if (key == '1'):
            print()
            print("Processing...")
            Webcam = cv2.VideoCapture(0)
            print("Ready for capturing images...")
            os.system("pause")
            CaptOpt(1)
        elif(key == '2'):
            print()
            print("Processing...")
            Webcam = cv2.VideoCapture(0)
            print("Ready for capturing images...")
            os.system("pause")
            CaptOpt(2)
        elif(key == '3'):
            print()
            print("Ready for model training...")
            os.system("pause")
            print()
            Model_Trainer.TrainModel()
        elif(key == '4'):
            print()
            print("Ready for preview...")
            os.system("pause")
            print()
            Run_Model.RunModel()
        elif(key == '5'):
            print()
            sys.exit("Exiting...")
    else:
        print()
        print("Please provide appropriate input!")
        sleep(2)
