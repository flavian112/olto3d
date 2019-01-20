import numpy as np
import cv2

import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

import src.paths
import src.filesystem

mapPath =  "../ressources/simplified/contourtest.jpg"
img = src.filesystem.readImg(mapPath)


plt.imshow(img, interpolation="bicubic")
plt.show()