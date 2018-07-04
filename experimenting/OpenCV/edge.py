import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    rtn, frame = cap.read()
    frame = cv2.resize(frame,(0, 0), fx=0.5, fy=0.5)

    laplacian = cv2.Laplacian(frame, cv2.CV_64F)
    sobely = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
    sobelx = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)
    edges = cv2.Canny(frame, 200, 200)

    #cv2.imshow('Original', frame)
    cv2.imshow('Laplacian', laplacian)
    cv2.imshow('Sobel x', sobelx)
    cv2.imshow('Sobel y', sobely)
    cv2.imshow('Canny', edges)


    k = cv2.waitKey(5)
    if k == ord('q'):
        break
cv2.destroyAllWindows()
cv2.waitKey(1)
cap.release()