import cv2
import os
import glob
import time
from os.path import isfile, join


print(os.listdir("Poses/"))

poses = os.listdir('Poses/')

for pose in poses:
    print(">> Working on pose : " + pose)
    subdirs = os.listdir('Poses/' + pose + '/')
    for subdir in subdirs:
        files = os.listdir('Poses/' + pose + '/' + subdir + '/')
        print(">> Working on examples : " + subdir)
        for file in files:
            if(file.endswith(".png")):
                path = 'Poses/' + pose + '/' + subdir + '/' + file
                path2 = path[:-4]
                # Read image
                im = cv2.imread(path)

                if not (file.endswith("_flipped.png")):
                    #オブジェクトimを左右反転しim2に代入
                    im2 = cv2.flip(im, 1)
                    cv2.imwrite(path2 + '_flipped.png' , im2)

                height, width, channels = im.shape
                if not height == width == 28:
                    # Resize image
                    im = cv2.resize(im, (28, 28), interpolation=cv2.INTER_AREA)
                    im2 = cv2.resize(im2, (28, 28), interpolation=cv2.INTER_AREA)
                    # im Write image
                    cv2.imwrite(path, im)
                    #im2 Write image
                    cv2.imwrite(path2 + '_flipped.png' , im2)
