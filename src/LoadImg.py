import cv2
import numpy as np
import os


def loadImg(path, size=(0,0), scale=(1,1)):
    loadedImg = cv2.imread(path)
    resizedImg = cv2.resize(loadedImg, size, fx=scale[0], fy=scale[1])
    return resizedImg

def loadImgFromDir(dir):
    imgs = []
    for imgname in sorted(os.listdir(dir)):
        img = cv2.imread(os.path.join(dir,imgname))
        if img is not None:
            imgs.append(img)
    return imgs

def rmFile(path):
    os.remove(path)