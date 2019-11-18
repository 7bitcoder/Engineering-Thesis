import cv2
from neuralNetwork import Net2, Net
import openCvTranforms.opencv_transforms.transforms as tf
import torchvision.transforms as transforms
from timeit import default_timer as timer
import torch
import numpy as np

# functions to show an image

cv2.namedWindow("preview")
vc = cv2.VideoCapture(2, cv2.CAP_DSHOW)

# width = vc.get(3)  # 640
# heigh = vc.get(4)  # 480
# fps = vc.get(5)  # 60

# new settings

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
    print(frame.shape)
else:
    rval = False
out = torch.zeros(10)
while rval:
    rval, frame = vc.read()
    # print(frame.shape)
    cv2.imshow("preview", frame)
    new_image = np.zeros((frame.shape[0], frame.shape[1]), np.int32)
    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            im = frame[y][x]
            new_image[y, x] = im[2] << 16 | im[1] << 8 | im[0]
    print(new_image[100:120,100:120])
    key = cv2.waitKey(1)
    if key == 27:  # exit on ESC
        break  # todo change to kayboard real time check
cv2.destroyWindow("preview")
