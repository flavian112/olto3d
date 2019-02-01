import cv2
import filesystem
import paths



def gen_neg(size=100):
    # Splices sample maps into 100x100 imgs and converts them to grayscale

    imgs = filesystem.readImgsFromDir(paths.SAMPLE)
    filesystem.createFolder(paths.NEG)

    img_idx = 0
    names = []

    for img in zip(range(len(imgs)), imgs):
        gray = cv2.cvtColor(img[1], cv2.COLOR_BGR2GRAY)
        h, w = gray.shape[:2]

        for i in range(h // size):
            for j in range(w // size):
                cy = i * size
                cx = j * size
                imgSplice = gray[cy:cy+size, cx:cx+size]

                name = "neg" + str(img_idx) + ".jpg"
                names.append(name)
                cv2.imwrite(paths.NEG + name, imgSplice)

                img_idx += 1


    # Generates file descriptor
    filesystem.removeFile(paths.DATA_PATH + "bg.txt")

    for name in names:
        lineToWrite = "neg/" + name + "\n"
        with open(paths.DATA_PATH + "/bg.txt", "a") as file:
            file.write(lineToWrite)

def genCascade():
    pass


gen_neg()




