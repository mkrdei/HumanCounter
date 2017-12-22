
import numpy as np
import math
import cv2
import winsound
import imutils

cap = cv2.VideoCapture('video.mp4')

#MOG2 kusurlu ama her platformda calisiyor.
fgbg = cv2.createBackgroundSubtractorMOG2(history=140, varThreshold=250)

#MOG kusursuz ama sadece Eclipse ve Spyderde calisiyor.
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history=100, backgroundRatio=0.3)

points = set()
#Alinan goruntuyu XVID formatinda kaydediyoruz.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('pedestrianOutput.avi',fourcc, 10, (1920,1080)) #Videonun boyut ve diger ozelliklerini tanimladik.
font = cv2.FONT_HERSHEY_SIMPLEX #Fonthershey fontunu kullaniyoruz

while(1):
    pointInMiddle = set()
    prev = points
    points = set()
    (grabbed, frame) = cap.read()
    if not grabbed:#Video bittiyse...
        print('Goruntu Sonlandi') #Goruntu sonlandi yazisini yazdirir.
        break #Program kapanir.
    frame = imutils.resize(frame, width=1366, height=768) #Goruntuyu tekrardan boyutlandirdim cunku ekrana sigmiyordu.
    fgmask = frame
    fgmask = cv2.blur(frame, (10,10)) #Bulaniklastirma maskesini de ekledik.
    fgmask = fgbg.apply(fgmask) #Maskemizi etkin hale getirdik.
    fgmask = cv2.medianBlur(fgmask, 7)
    oldFgmask = fgmask.copy()
    image, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,1)
    if len(prev) == 5: #Eger 5 kisi olduysa...
        cv2.putText(frame, '5 KISI OLDU!!!', (1100,400), font , 1, (75,0,130), 3, cv2.LINE_AA)#5 kisi oldugunda uyariyi veriyoruz.
        frequency = 2500  # Frekansi 2500 yaptik
        duration = 100  # 0.1 saniye boyunca alarm calacak.
        winsound.Beep(frequency, duration) #Bip sesinin cikmasini saglayan fonksiyon.
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w>70 and h>80:#Eger boyutlarimiz bu kosula uyarsa dikdortgeni cizecek.
            cv2.rectangle( frame,(x,y), (x+w,y+h), (128,0,128), 2, lineType=cv2.LINE_AA)#Insanlarin etrafina dikdortgen cizdiriyoruz.
            point = (int(x+w/2.0), int(y+h/2.0))#dikdortgenlerin tam ortasina pointimizi atiyoruz.
            points.add(point)#points kumesine pointimizi ekliyoruz.
    for point in points:#points icindeki her point icin
        (xnew, ynew) = point # Bu arada xnew ve ynew diye yeni bir koordinat degeri olusturuldu ve pointimizin koordinatlarini bu degerlerde tutacagiz.
        cv2.circle(frame, point, 3, (255,0,0),6)#Pointimizin rengini ve boyutunu belirterek ekrana cizdiriyoruz.
    cv2.putText(frame,'KAC KISI VAR?', (1100,200), font, 1, (75,0,130), 2, cv2.LINE_AA) #Kac kisi var yazisini ekrana yazdirdik.
    cv2.putText(frame, '' + str(len(prev)), (1200,300), font , 2, (75,0,130), 3, cv2.LINE_AA) #Kac kisi oldugunu rakamsal olarak yazdirdik.
    cv2.imshow('a',oldFgmask) #Maskeli goruntuyu actik. 
    cv2.imshow('',frame)  #Goruntuyu ekranda aciyoruz
    out.write(frame)
    l = cv2.waitKey(1) & 0xff #waitKey videonun hizini ayarayabilmemizi sagliyor.
    if l == 27: #esc'ye basilirsa program kapanir
        break
cap.release()#Goruntuyu kapat.
cv2.destroyAllWindows()#Butun ekranlari yok et.
