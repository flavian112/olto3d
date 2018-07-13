import cv2
import numpy as np

s = 0.3

org = cv2.imread('mapdata/map1.jpg')
img = cv2.resize(org, (0, 0), fx=1, fy=1)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
cont = cv2.cvtColor(blur, cv2.COLOR_GRAY2RGB)

hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
lower = np.array([0, 0, 0]) #lower = np.array([15, 50, 20]) ## hsv
upper = np.array([255, 255, 200]) #upper = np.array([30, 100, 100]) ##hsv
bluefiltermask = cv2.inRange(hsv, lower, upper)
edgesOnMask = cv2.Canny(bluefiltermask, 100, 100)


#res = cv2.bitwise_and(gray, gray, mask=mask)
#cv2.imshow('Mask', mask)
#cv2.imshow('Res', res)

def displayImg(pic, scale, title):
    cv2.imshow(title, cv2.resize(pic, (0, 0), fx=scale, fy=scale))

displayImg(bluefiltermask, s, 'Mask')
displayImg(edgesOnMask, s, 'Edges on Mask')


edges = cv2.Canny(blur, 100, 100)
im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

lens = list(map(len , contours))
filtered_contours = list(filter(lambda x: len(x) > 100, contours))

print(sum(lens)/len(lens))
print(hierarchy)

cv2.drawContours(cont, filtered_contours, -1, (42,65,156), 3)

displayImg(img, s, 'Original')
displayImg(cont, s, 'Contours')
#displayImg(edges, s, 'Edges')


cv2.waitKey(0)
cv2.destroyAllWindows()
