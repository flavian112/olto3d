import cv2
import numpy as np
from LoadImg import *

MAPS_PATH = "../ressources/maps/"
MAP_PATH = MAPS_PATH + "map3.jpg"

img = loadImg(MAP_PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
gray_filtered = cv2.inRange(gray, 60, 140)
#thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

height, width, channels = img.shape
blank_image = np.zeros((height, width,1), np.uint8)

lower_brown = np.array([0, 50, 50])
upper_brown = np.array([20, 255, 255])

mask = cv2.inRange(hsv, lower_brown, upper_brown)


mask3 = cv2.bitwise_and(gray_filtered,gray_filtered, mask= mask)

image, contours, hierarchy = cv2.findContours(mask3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


laplacian = cv2.Laplacian(mask3, cv2.CV_64F)
sobely = cv2.Sobel(mask3, cv2.CV_64F, 1, 0, ksize=5)
sobelx = cv2.Sobel(mask3, cv2.CV_64F, 0, 1, ksize=5)
edges = cv2.Canny(mask3, 200, 200)

lens = list(map(len , contours))
filtered_contours = list(filter(lambda x: len(x) > 20, contours))

grayBGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
cv2.drawContours(blank_image, filtered_contours, -1, (255,255,255), 5)


cv2.imshow("Map", cv2.resize(blank_image, (0,0), fx=0.3, fy=0.3))
cv2.waitKey(0)
cv2.destroyAllWindows()