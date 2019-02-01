import numpy as np
import cv2


from random import *

import sys
from copy import deepcopy as deepcopy

import filesystem
import colladaExport as dae


helptxt = "Command usage: olto3d [numberOfCheckpoints] [input.jpg] [output.dae]"
args = sys.argv
print()

if len(args) < 4:
    print(helptxt)
    sys.exit(0)

inputpath = args[2]
outputpath = args[3]
numberOfCheckpoints = int(args[1])


print("reading file...")
img = filesystem.readImg(inputpath)
# Convert color from bgr to rgb (Opencv uses default bgr / Matplotlib uses default rgb)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
scale3d = 0.1

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

height, width, channels = img.shape

blank_image = np.zeros((height, width,1), np.uint8)






print("generating hmap...")

# Convert color to hsv for better color filtering
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

# Define color range (hsv (hue channel)) for brown tones
lower_brown = np.array([0, 50, 50])
upper_brown = np.array([20, 255, 255])

# Create Bitmask for brown parts of image
filteredBrownsmask = cv2.inRange(hsv, lower_brown, upper_brown)

# Apply Mask to black and white image
contourimg = cv2.bitwise_and(gray, gray, mask=filteredBrownsmask)


# Find contours and its hierarchy
contours, hierarchy = cv2.findContours(contourimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

hierarchy = hierarchy[0]

hmap = deepcopy(blank_image)


# Set height for each contour
def fillcontours(hier, conts, img, idx=0, iterations=0):
    curr = hier[idx]
    cont = conts[idx]
    next = curr[0]
    child = curr[2]

    l = cont.shape[0]

    points = np.empty((l, 2), dtype=np.uint8)

    for ptsn in enumerate(cont):
        i, pts = ptsn
        x, y = pts[0][0], pts[0][1]
        points[i][0] = y
        points[i][0] = x

    colorStep = 255 // len(conts)
    c = colorStep * iterations
    cv2.fillPoly(img, pts=[cont], color=(c, c, c))

    if (child >= 0):
        fillcontours(hier, conts, img, child, iterations=iterations + 1)

    if (next >= 0):
        fillcontours(hier, conts, img, next, iterations=iterations)


# Find top contour of hierarchy
def findFirst(hier):
    curr = hier[0]
    idx = 0
    lastidx = 0
    while (curr[3] >= 0):
        curr = hier[curr[3]]
        lastidx = idx
        idx = curr[3]
    while (curr[1] >= 0):
        curr = hier[curr[1]]
        lastidx = idx
        idx = curr[1]

    return lastidx


# Too many recursions for big images
sys.setrecursionlimit(1000000)

idx = findFirst(hierarchy)
fillcontours(hierarchy, contours, blank_image, idx=idx)

# Resize hmap for faster processing
hmap = cv2.resize(hmap, (0, 0), fx=scale3d, fy=scale3d, interpolation=cv2.INTER_AREA)

kernelsize = int((width + height) * scale3d) // 2 + 1

# Gaussian blur to smoothen heightmap
hmap = cv2.GaussianBlur(hmap, (kernelsize, kernelsize), 0)

hmapimg = cv2.cvtColor(hmap, cv2.COLOR_GRAY2BGR)


print("detect checkpoints...")
# Filtering color of checkpoints
mask1 = cv2.inRange(hsv, np.array([0,70, 50]), np.array([0, 255, 255]))
mask2 = cv2.inRange(hsv, np.array([170, 70, 50]), np.array([180, 255, 255]))
mask = mask1 | mask2

# Detect circles
circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 30,
                           param1=30,
                           param2=15,
                           minRadius=10,
                           maxRadius=70)

imgToDraw = deepcopy(img)

# Number of best detected circles that should be drawn


# Draw circles to map
if circles != [] or circles != None:
    circles = np.uint16(np.around(circles))

    for circle in circles[0][:numberOfCheckpoints]:
        cv2.circle(imgToDraw, (circle[0], circle[1]), 100, (0, 0, 255), 10)


print("detect trees...")
mask = cv2.inRange(hsv, np.array([60, 70, 150]), np.array([80, 255, 255]))

# Dilute tree areas
kernelsize = int((height+width/2)*0.002) + 1
kernel = np.ones((kernelsize,kernelsize),np.uint8)
mask = cv2.dilate(mask, kernel, iterations = 2)

# Define how dense the trees should be drawn
treedensity=5

# Create treemap
treesresized = cv2.resize(mask.copy(), (0,0), fx=scale3d/treedensity, fy=scale3d/treedensity,interpolation = cv2.INTER_AREA)
ret, treemap = cv2.threshold(treesresized,127,255,cv2.THRESH_BINARY)

print("Creating collada model...")
mesh = dae.createMesh()
mesh = dae.createTerrain(hmap, mesh)
mesh = dae.addRessourcesToMesh(mesh, dae.tree)
mesh = dae.addRessourcesToMesh(mesh, dae.checkpoint)

s = scale3d / treedensity
cords = []
for x in range(treemap.shape[0]):
    for z in range(treemap.shape[1]):
        y = hmap[x * treedensity][z * treedensity]

        if (treemap[x][z] > 0):
            randomxdeflection = uniform(-treedensity, treedensity)
            randomzdeflection = uniform(-treedensity, treedensity)

            x_t = (x * treedensity + randomxdeflection)
            z_t = (z * treedensity + randomzdeflection)

            cords.append((x_t, y, z_t))

mesh = dae.addObjToMesh(mesh, dae.tree, 'tree', cords, scale=(s, s, s), rotation=(np.pi, 0, 0))

s = scale3d
cords = []
if (circles != []):
    for circle in circles[0][:numberOfCheckpoints]:
        z = int(circle[0]) * s
        x = int(circle[1]) * s
        y = hmap[int(x)][int(z)]

        cords.append((x, y, z))


mesh = dae.addObjToMesh(mesh, dae.checkpoint, 'checkpoint', cords, scale=(s, s, s), rotation=(0, 0, 0))

mesh.write(outputpath)

print("Done")