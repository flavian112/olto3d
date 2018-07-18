import cv2
import os


def readImg(path, size=(0,0), scale=(1,1)): # Reads img from disk into memory
    try:
        loadedImg = cv2.imread(path)
        resizedImg = cv2.resize(loadedImg, size, fx=scale[0], fy=scale[1])
        return resizedImg
    except:
        print("Error while reading image with path: " + path)

def writeImg(path, img, override=True): # Writes img from memory to disk
    if os.path.isfile(path):
        if override:
            removeFile(path)
            writeImg(path, img)
    else:
        cv2.imwrite(path, img)


def readImgsFromDir(dir): # Reads multiple sampleImgs from dir into memory
    imgs = []
    for imgname in sorted(os.listdir(dir)):
        img = readImg(os.path.join(dir,imgname))
        if img is not None:
            imgs.append(img)
    return imgs

def removeFile(path): # Removes file if it exists
    if os.path.isfile(path):
        os.remove(path)

def createFolder(path): # Creates folder if it doesn't exist
    if not os.path.isdir(path):
        os.mkdir(path)