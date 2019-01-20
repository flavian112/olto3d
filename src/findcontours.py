import numpy as np
import cv2

import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

import src.paths
import src.filesystem

mapPath =  "../ressources/simplified/contourtest.jpg"
img = src.filesystem.readImg(mapPath)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

height, width, channels = img.shape

blank_image = np.zeros((height, width,1), np.uint8)

plt.figure(figsize=[10,10])
plt.axis('off')
plt.imshow(img, interpolation="bicubic")
