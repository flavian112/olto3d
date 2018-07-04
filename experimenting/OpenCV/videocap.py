import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    center = frame[100:400,100:500]
    frame[0:300, 0:400] = center


    cv2.imshow('Face Cam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()