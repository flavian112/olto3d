import cv2
import numpy as np

cap = cv2.VideoCapture('people-walking.mp4')
#cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    rtn, frame = cap.read()
    fgmask = fgbg.apply(frame)

    cv2.imshow('Original', frame)
    cv2.imshow('Fg', fgmask)

    k = cv2.waitKey(30)
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()