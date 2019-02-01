import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    rtn , frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    lower_red = np.array([120,130,50])
    upper_red = np.array([180,255,150])

    #kernel = np.ones((15,15), np.float32)/255

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    #smoothed = cv2.filter2D(res, -1, kernel)
    blur = cv2.GaussianBlur(res, (15,15), 0)
    median = cv2.medianBlur(res, 15)
    bilateral = cv2.bilateralFilter(res, 15, 75, 75)

    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    dilation = cv2.dilate(mask,kernel, iterations=1)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)



    #cv2.imshow('Frame', frame)
    #cv2.imshow('Mask', mask)
    cv2.imshow('Result', res)
    #cv2.imshow('Blur', median)
    #cv2.imshow('Erosion', erosion)
    #cv2.imshow('Dilation', dilation)
    cv2.imshow('Opening', opening)
    cv2.imshow('Closing', closing)

    k = cv2.waitKey(5)
    if k == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()