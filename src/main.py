import cv2
import numpy as np
from LoadImg import *

MAPS_PATH = "../ressources/maps/"
MAP_PATH = MAPS_PATH + "map1.jpg"

img = loadImg(MAP_PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
gray_filtered = cv2.inRange(gray, 60, 140)
#thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)


lower_brown = np.array([0, 50, 50])
upper_brown = np.array([20, 255, 255])

mask = cv2.inRange(hsv, lower_brown, upper_brown)


mask3 = cv2.bitwise_and(gray_filtered,gray_filtered, mask= mask)

image, contours, hierarchy = cv2.findContours(mask3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


lens = list(map(len , contours))
filtered_contours = list(filter(lambda x: len(x) > 10, contours))

grayBGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
cv2.drawContours(grayBGR, filtered_contours, -1, (255,0,0), 3)


cv2.imshow("Map", cv2.resize(grayBGR, (0,0), fx=0.3, fy=0.3))
cv2.waitKey(0)
cv2.destroyAllWindows()