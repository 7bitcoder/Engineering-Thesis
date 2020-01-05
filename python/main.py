from _testbuffer import ndarray

import cv2
from neuralNetwork import Net2, Net
import openCvTranforms.opencv_transforms.transforms as tf
import torchvision.transforms as transforms
import torch
from PyQt5.QtCore import *
from time import time
from mainCuda import globNr
from comunication import Commands

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
        self.width = 60
        self.heigh = 60
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        self.maxLen = 200
        self.step = 30.1
        self.offset = 5
        self.offset2 = 44
        self.printFps = print
        self.thicc = 10
        self.device = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.net = Net(self.width, self.heigh)
        self.transform = transforms.Compose([
            tf.Resize((self.heigh, self.width)),
            tf.ToTensor(),
            tf.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        self.signals = Signals()
        self.running = True
        self.signals.finished.connect(self.stop)
        self.cameraHeigh = int(self.device.get(4))  # 480
        self.cameraWidth = int(self.device.get(3))  # 640
        self.cut = self.cameraWidth - self.cameraHeigh
        self.alpha = 0.2
        self.disableNetwork = False

    def stop(self):
        self.running = False

    def drawStatistics(self, image, stats, chosen):
        copy = image.copy()
        cv2.rectangle(copy, (0, 0), (self.cut, self.cameraHeigh), (128, 128, 128), cv2.FILLED)
        image = cv2.addWeighted(image, self.alpha, copy, 1 - self.alpha, gamma=0)
        for i, data in enumerate(stats.view(-1)):
            cv2.rectangle(image, (self.offset, int(self.offset2 + i * self.step)),
                          (self.offset + (data * self.maxLen), int(i * self.step) + self.thicc + self.offset2),
                          self.colors[i % 3], -1)
        return image

    def imshow(self, img):
        img = img.view(self.heigh, self.width, 1).numpy() / 2 + 0.5  # unnormalize
        print(img.shape)
        # npimg = img.numpy()
        # cv2.imshow("preview", img)

    def run(self):
        try:
            scale = 2.5
            # width = vc.get(3)  # 640
            # heigh = vc.get(4)  # 480
            # fps = vc.get(5)  # 60

            # new settings

            self.device.set(5, 30)  # set fps
            # print(self.device.get(16))
            # self.device.set(16, 1)  #set to rgb

            # print("width: " + str(self.device.get(3)) + " heigh: " + str(self.device.get(4)))

            self.net = torch.load("./savedMode{}.pth".format(globNr.nr))
            self.net.eval()

            if self.device.isOpened():  # try to get the first frame
                rval, frame = self.device.read()
            # print(frame.shape)
            else:
                rval = False
            out = torch.zeros(13)
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
                ###
                #rval = True
                #command = Commands.commands.biggerTurnAngle
                #number = 21
                #frame = cv2.imread(r"D:\DataSetNew\{}\SD\{}_{}.jpg".format(command.name, command.value, number))
                ###
                frame = cv2.flip(frame, 1)
                frameWithStats = frame.copy()
                frameWithStats = cv2.cvtColor(frameWithStats, cv2.COLOR_BGR2RGB)
                frame = frame[:, self.cut:self.cameraWidth]
                frame = self.transform(frame).view(-1, 3, self.heigh, self.width)
                if not self.disableNetwork:
                    out = self.net(frame)
                else:
                    out = torch.zeros(13)
                frameWithStats = self.drawStatistics(frameWithStats, out, 1)
                self.signals.result.emit(frameWithStats, out)
        except Exception as e:
            print(e)
        finally:
            pass
