import cv2
import numpy as np



def loadImg(path, size=(0,0), scale=(1,1)):
    loadedImg = cv2.imread(path)
    resizedImg = cv2.resize(loadedImg, size, fx=scale[0], fy=scale[1])
    return resizedImg