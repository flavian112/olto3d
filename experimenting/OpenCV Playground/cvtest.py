import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('faceImg.jpg', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray', interpolation='bicubic')
plt.plot([200,400],[320, 400], 'c', linewidth=5)
plt.show()

