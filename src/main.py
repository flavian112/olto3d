import cv2
import numpy as np
import filesystem
import paths


def find_skeleton3(img): #https://stackoverflow.com/questions/42845747/optimized-skeleton-function-for-opencv-with-python#42846932
    skeleton = np.zeros(img.shape,np.uint8)
    eroded = np.zeros(img.shape,np.uint8)
    temp = np.zeros(img.shape,np.uint8)

    _,thresh = cv2.threshold(img,127,255,0)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

    iters = 0
    while(True):
        cv2.erode(thresh, kernel, eroded)
        cv2.dilate(eroded, kernel, temp)
        cv2.subtract(thresh, temp, temp)
        cv2.bitwise_or(skeleton, temp, skeleton)
        thresh, eroded = eroded, thresh # Swap instead of copy

        iters += 1
        if cv2.countNonZero(thresh) == 0:
            return (skeleton,iters)


mapPath =  paths.MAPS_PATH + "map1.jpg"

img = filesystem.readImg(mapPath)
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


blur = cv2.GaussianBlur(mask3, (31,31), 1)
kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(blur,kernel,iterations = 1)
skel = find_skeleton3(dilation)[0]

laplacian = cv2.Laplacian(mask3, cv2.CV_64F)
sobely = cv2.Sobel(mask3, cv2.CV_64F, 1, 0, ksize=5)
sobelx = cv2.Sobel(mask3, cv2.CV_64F, 0, 1, ksize=5)
edges = cv2.Canny(mask3, 200, 200)

image, contours, hierarchy = cv2.findContours(skel,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)




filtered_contours = list(filter(lambda x: len(x) > 0, contours))#[:100]
filtered_contours.sort(key=len, reverse=True)



grayBGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
cv2.drawContours(blank_image, filtered_contours[:100], -1, (255, 255, 255), thickness=3)





checkpoint_cascade = cv2.CascadeClassifier('../ressources/cascades/cascade_checkpoint2_10.xml')
checkpoints = checkpoint_cascade.detectMultiScale(gray, 1.5, 5)

for (x,y,w,h) in checkpoints:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)


contours_endpoints = []

def dist(point1, point2):
    return np.linalg.norm(point1 - point2)





points = []
for contour in filtered_contours:
    for point in contour:
        points.append(point)



    begin = contour[0][0]
    end = contour[-1][0]

    contours_endpoints.append([begin, end])




hull = cv2.convexHull(np.array(points))


#cv2.drawContours(grayBGR, [hull], -1, (0, 0, 255), 5)


#for point in points:
#    x = point[0][0]
#    y = point[0][1]
#    cv2.circle(grayBGR, (x, y), 2, (0,0,255), thickness=cv2.FILLED)




for i, endpoints1 in enumerate(reversed(contours_endpoints)):
    d = 1000000
    b1x, b1y = endpoints1[0][0], endpoints1[0][1]
    e1x, e1y = endpoints1[1][0], endpoints1[1][1]
    for j, endpoints2 in enumerate(contours_endpoints):
        b1x, b1y = endpoints2[0][0], endpoints2[0][1]
        e1x, e1y = endpoints2[1][0], endpoints2[1][1]
        #cd = dist()







    #cv2.circle(grayBGR, (bx, by), 10, (0, 255, 0), thickness=cv2.FILLED)
    #cv2.circle(grayBGR, (ex, ey), 10, (255, 0, 0), thickness=cv2.FILLED)


    #for j, endpoints2 in enumerate(contours_endpoints):




cv2.imshow("Skel", cv2.resize(blank_image, (0,0), fx=0.3, fy=0.3))

#cv2.imshow("Contours", cv2.resize(dilation, (0,0), fx=0.3, fy=0.3))
#cv2.imshow("Mask", cv2.resize(mask3, (0,0), fx=0.3, fy=0.3))
cv2.waitKey(0)
cv2.destroyAllWindows()