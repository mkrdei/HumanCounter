import numpy as np
import math
import cv2
import winsound
import imutils

cap = cv2.VideoCapture('vid2Trim.mp4')
#fgbg = cv2.createBackgroundSubtractorMOG2(history=140, varThreshold=250)
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history=100, backgroundRatio=0.3)

def line1(x,y):
    return y - (29*x)/96.0 - 300

def line2(x,y):
    return y - (29*x)/96.0 - 500



points = set()
pointFromAbove = set()
pointFromBelow = set()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('pedestrianOutput.avi',fourcc, 10, (1920,1080))
font = cv2.FONT_HERSHEY_SIMPLEX

while(1):
    pointInMiddle = set()
    prev = points
    points = set()
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=1366, height=768)
    fgmask = frame
    fgmask = cv2.blur(frame, (10,10))
    fgmask = fgbg.apply(fgmask)
    fgmask = cv2.medianBlur(fgmask, 7)
    oldFgmask = fgmask.copy()
    image, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,1)
    if len(prev) == 5:
        cv2.putText(frame, '5 KISI OLDU!!!', (1100,400), font , 1, (75,0,130), 3, cv2.LINE_AA)
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 300  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w>70 and h>80:#Eger boyutlarimiz bu kosula uyarsa cerceveyi cizdirecegiz.
            cv2.rectangle( frame,(x,y), (x+w,y+h), (128,0,128), 2, lineType=cv2.LINE_AA)#Insanlarin etrafina dikdortgen cizdiriyoruz.
            point = (int(x+w/2.0), int(y+h/2.0))#dikdortgenlerin tam ortasina noktalarimizi koyuyoruz.
            points.add(point)#points kumesine pointimizi ekliyoruz.
    for point in points:#points icindeki her point icin:
        (xnew, ynew) = point
        if line1(xnew, ynew) > 0 and line2(xnew, ynew) < 0:
            pointInMiddle.add(point)
        for prevPoint in prev:
            (xold, yold) = prevPoint
            dist = cv2.sqrt((xnew-xold)*(xnew-xold)+(ynew-yold)*(ynew-yold))
            if dist[0] <= 120:
                if line1(xnew, ynew) >= 0 and line2(xnew, ynew) <= 0:
                    if line1(xold, yold) < 0: # Nokta yukaridaki cizgiden giris yaparsa.
                        pointFromAbove.add(point)
                    elif line2(xold, yold) > 0: # Nokta asagidaki cizgiden giris yaparsa.
                        pointFromBelow.add(point)
                    else:   # Zaten cizgilerin arasindaysa.
                        if prevPoint in pointFromBelow:
                            pointFromBelow.remove(prevPoint)
                            pointFromBelow.add(point)

                        elif prevPoint in pointFromAbove:
                            pointFromAbove.remove(prevPoint)
                            pointFromAbove.add(point)

                if line1(xnew, ynew) < 0 and prevPoint in pointFromBelow: # Point is above the line
                    pointFromBelow.remove(prevPoint)

                if line2(xnew, ynew) > 0 and prevPoint in pointFromAbove: # Point is below the line
                    pointFromAbove.remove(prevPoint)



            cv2.circle(frame, point, 3, (105,105,105),6)
    cv2.putText(frame,'KAC KISI VAR?', (1100,200), font, 1, (75,0,130), 2, cv2.LINE_AA)
    cv2.putText(frame, '' + str(len(prev)), (1200,300), font , 2, (75,0,130), 3, cv2.LINE_AA)
    cv2.imshow('a',oldFgmask)     
    cv2.imshow('',frame)  
    out.write(frame)
    l = cv2.waitKey(1) & 0xff
    
    if l == 27:
        break
cap.release()
cv2.destroyAllWindows()