import cv2
import numpy as np

from Color_Picker import h_max, h_min, s_min, s_max, v_min, v_max

###################### READ WEBCAM ######################
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,180)

myColors = [[5,107,0,19,255,255], #Orange
            [133,56,0,159,156,255], #Purple
            [57,76,0,100,255,255]] #Green

myColorValues = [[51,153,255], ## BGR
                 [255,0,255], # Purple
                 [0,255,0]] #Green

myPoints = [] ## [x , y , colorID]

def findColor(img, myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)  # it will filter out and give us filtered out image of that color
        x, y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x,y,count])
        count += 1
        #cv2.imshow(str(color[0]), mask)
    return newPoints

def getContours(img): #Iterate over contours, not contours.hierarchy.
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  #pixels
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            para = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*para,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP) #it is a list and we need to break it down to points again so we have this loop here
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
