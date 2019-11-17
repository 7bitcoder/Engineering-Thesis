import cv2
from neuralNetwork import Net2, Net
import openCvTranforms.opencv_transforms.transforms as tf
import torchvision.transforms as transforms
from timeit import default_timer as timer
import torch
import numpy as np

# functions to show an image

width = 160
heigh = 120
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
labels = ['0','1','2','3','4','5','6','7','8','9'];
maxLen = 200
step = 40
offset = 5
thicc = 20


def drawStatistics(image, stats, chosen):
    for i, data in enumerate(stats.view(-1)):
        imm = 10
        cv2.rectangle(image, (offset, i * step), (offset + (data * maxLen), (i * step) + thicc), colors[i % 3], -1)
        cv2.putText(image, labels[i], (offset, i * step + 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                    color=(255, 255, 255), thickness=1, lineType=-1)
    nnm = 20


def imshow(img):
    img = img.view(heigh, width, 1).numpy() / 2 + 0.5  # unnormalize
    print(img.shape)
    # npimg = img.numpy()
    cv2.imshow("preview", img)


cv2.namedWindow("preview")
vc = cv2.VideoCapture(0, cv2.CAP_DSHOW)
scale = 2.5
# width = vc.get(3)  # 640
# heigh = vc.get(4)  # 480
# fps = vc.get(5)  # 60

# new settings

vc.set(5, 24)  # set fps

print("width: " + str(vc.get(3)) + " heigh: " + str(vc.get(4)))
device = torch.device("cuda:0");
net = Net(width, heigh).to(device)
net = torch.load("./savedModel.pth")
net.eval()

transform = transforms.Compose(
    [tf.Grayscale(),
     tf.Scale((heigh, width)),
     tf.ToTensor(),
     tf.Normalize((0.5,), (0.5,))
     ])

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
    print(frame.shape)
else:
    rval = False
out = torch.zeros(10)
while rval:
    start = timer()
    rval, frame = vc.read()
    # print(frame.shape)
    drawStatistics(frame, out, 1)
    cv2.imshow("preview", frame)
    frame = transform(frame).view(-1, 1, heigh, width)
    print(frame.shape)
    # imshow(frame)
    out = net(frame.to(device))
    print(out.shape)
    end = timer()
    print(end - start)
    key = cv2.waitKey(1)
    if key == 27:  # exit on ESC
        break  # todo change to kayboard real time check
cv2.destroyWindow("preview")
