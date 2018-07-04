import cv2
import numpy as np

watch_cascade = cv2.CascadeClassifier('cascade_watch.xml')

cap = cv2.VideoCapture(0)

while True:
    rtn, img = cap.read()
    img = cv2.resize(img,(0, 0), fx=0.5, fy=0.5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    watches = watch_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in watches:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),2)

    cv2.imshow('Watch', img)
    k = cv2.waitKey(30)
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()