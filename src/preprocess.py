import cv2
import numpy as np
from LoadImg import *

DATA_PATH = "../ressources/datasets/"



def gen_neg(size=100):
    imgs = loadImgFromDir(DATA_PATH + "imgs")

    img_idx = 0
    names = []
    for img in zip(range(len(imgs)), imgs):
        gray = img[1]#cv2.cvtColor(img[1], cv2.COLOR_BGR2GRAY)

        h, w = gray.shape[:2]
        cropped_img = gray[0:h-h%size, 0:w-w%size]

        h, w = cropped_img.shape[:2]

        for i in range(h // size):
            for j in range(w // size):
                cy = i * size
                cx = j * size
                name = str(img_idx) + ".jpg"
                names.append(name)
                recropped_img = cropped_img[cy:cy+size, cx:cx+size]
                cv2.imwrite(DATA_PATH + "neg/" + name, recropped_img)
                img_idx += 1
    rmFile(DATA_PATH + "/bg.txt")

    for name in names:
        lineToWrite = "neg/" + name + "\n"
        with open(DATA_PATH + "/bg.txt", "a") as file:
            file.write(lineToWrite)


gen_neg()




