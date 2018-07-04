import urllib.request
import cv2
import numpy as np
import os

def store_raw_images():
    #http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152
    #http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513
    neg_images_link='http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()

    if not os.path.exists('neg'):
        os.makedirs('neg')

    pic_num = 918

    for i in neg_image_urls.split('\n'):
        try:
            img_path = 'neg/'+str(pic_num)+'.jpg'
            print(i)
            urllib.request.urlretrieve(i, img_path)
            img =cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(img, (100,100))
            cv2.imwrite(img_path, resized_image)
            pic_num += 1
        except Exception as e:
            print(str(e))
store_raw_images()
