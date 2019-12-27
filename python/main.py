from _testbuffer import ndarray

import cv2
from neuralNetwork import Net2, Net
import openCvTranforms.opencv_transforms.transforms as tf
import torchvision.transforms as transforms
import torch
from PyQt5.QtCore import *
from time import time

# functions to show an image
class Signals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object, torch.Tensor)


class GestureRecognition(QThread):
    """main class with neural network"""

    def __init__(self, print):
        super(GestureRecognition, self).__init__()
        self.width = 80
        self.heigh = 60
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                       '18', '19',
                       '20', '21', '22', '23', '24', '25', '26']
        self.maxLen = 200
        self.step = 20
        self.offset = 5
        self.printFps = print
        self.thicc = 10
        self.device = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.net = Net(self.width, self.heigh)
        self.transform = transforms.Compose(
            [tf.Grayscale(),
             tf.Resize((self.heigh, self.width)),
             tf.ToTensor(),
             tf.Normalize((0.5,), (0.5,))
             ])
        self.signals = Signals()
        self.running = True
        self.signals.finished.connect(self.stop)

    def stop(self):
        self.running = False

    def drawStatistics(self, image, stats, chosen):
        for i, data in enumerate(stats.view(-1)):
            imm = 10
            cv2.rectangle(image, (self.offset, i * self.step),
                          (self.offset + (data * self.maxLen), (i * self.step) + self.thicc), self.colors[i % 3], -1)
            cv2.putText(image, self.labels[i], (self.offset, i * self.step + 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(255, 255, 255), thickness=1, lineType=-1)
        nnm = 20

    def imshow(self, img):
        img = img.view(self.heigh, self.width, 1).numpy() / 2 + 0.5  # unnormalize
        print(img.shape)
        # npimg = img.numpy()
        # cv2.imshow("preview", img)

    def run(self):
        scale = 2.5
        # width = vc.get(3)  # 640
        # heigh = vc.get(4)  # 480
        # fps = vc.get(5)  # 60

        # new settings

        self.device.set(5, 25)  # set fps
        #print(self.device.get(16))
        #self.device.set(16, 1)  #set to rgb

        #print("width: " + str(self.device.get(3)) + " heigh: " + str(self.device.get(4)))

        self.net = torch.load("./savedMode2.pth")
        self.net.eval()

        if self.device.isOpened():  # try to get the first frame
            rval, frame = self.device.read()
           # print(frame.shape)
        else:
            rval = False
        out = torch.zeros(27)
        start = time()
        fps = 0
        while rval and self.running:
            if time() - start < 1:
                fps += 1
            else:
                start = time()
                self.printFps(fps)
                fps = 0
            rval, frame = self.device.read()
            # frame = cv2.imread(r'./kinect_leap_dataset/acquisitions/P1/G1/0_rgb.png')
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frameWithStats = frame.copy()
            #print(frameWithStats.shape)
            self.drawStatistics(frameWithStats, out, 1)
            # cv2.imshow("preview", frameWithStats)
            frame = self.transform(frame).view(-1, 1, self.heigh, self.width)
            #print(frame.shape)
            #imshow(frame)
            out = self.net(frame)
            self.signals.result.emit(frameWithStats, out)
            #print(out.shape)