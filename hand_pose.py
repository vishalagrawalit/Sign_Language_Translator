import cv2
import numpy as np
import re

# Importing our dependencies
import util as ut
import svm_train as st

import time

# create and train SVM model each time coz bug in opencv 3.1.0 svm.load() https://github.com/Itseez/opencv/issues/4969
model = st.trainSVM(9, 20, 'TrainData2')
move_text = {'1': 'GRAB', '2': 'Bless', '3': 'Rock', '4': 'Stop', '5': 'ThumbsUp', '6': 'Victory', '7': 'Stop2',
             '8': 'Left', '9': 'Right'}

# Camera and font initialization
cam = int(input("Enter Camera Index : "))
cap = cv2.VideoCapture(cam)
font = cv2.FONT_HERSHEY_SIMPLEX


temp = 0
previouslabel = None
previousText = " "
label = None
text = ""
while (cap.isOpened()):
    move = ''
    t = time.time()
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th1 = cv2.threshold(gray.copy(), 150, 255, cv2.THRESH_TOZERO)
    cv2.imshow('thresh', th1)
    _, contours, hierarchy = cv2.findContours(th1.copy(), cv2.RETR_EXTERNAL, 2)
    cnt = ut.getMaxContour(contours, 4000)
    if cnt.any() != None:
        gesture, label = ut.getGestureImg(cnt, img, th1, model)

        if label != None:
            if temp == 0:
                previouslabel = label
        if previouslabel == label:
            previouslabel = label
            temp += 1
        else:
            temp = 0
        if (temp == 40):
            if (label == 'P'):
                label = " "
            text += label
            if (label == 'Q'):
                words = re.split(" +", text)
                words.pop()
                text = " ".join(words)
            # text=previousText
            print(text)

        cv2.imshow('PredictedGesture', cv2.imread('TrainData2/' + label + '_1.jpg'))  # showing the best match or prediction
        cv2.putText(img, label, (50, 150), font, 8, (0, 125, 155),
                    2)  # displaying the predicted letter on the main screen
        cv2.putText(img, text, (50, 450), font, 3, (0, 0, 255), 2)

    fps = int(1 / (time.time() - t))
    cv2.putText(img, "FPS: " + str(fps) + move, (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Frame', img)
    k = 0xFF & cv2.waitKey(10)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()