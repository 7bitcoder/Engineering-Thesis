from _testbuffer import ndarray

import cv2
import torch
import os
from time import time
from enum import Enum
from comunication import Commands
if __name__ == '__main__':

    device = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    device.set(5, 60)  # set fps

    width = int(device.get(3))  # 640
    heigh = int(device.get(4))  # 480
    # fps = vc.get(5)  # 60
    # print(self.device.get(16))
    # self.device.set(16, 1)  #set to rgb

    print("width: " + str(device.get(3)) + " heigh: " + str(device.get(4)))
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
              '18', '19',
              '20', '21', '22', '23', '24', '25', '26']
    maxLen = 200
    step = 20
    offset = 5
    printFps = print
    thicc = 10
    cut = width - heigh
    alpha = 0.2


    def drawStatistics(image, stats, chosen):
        copy = image.copy()
        cv2.rectangle(copy, (0, 0), (cut, heigh), (128, 128, 128), cv2.FILLED)
        image = cv2.addWeighted(image, alpha, copy, 1 - alpha, gamma=0)
        # for i, data in enumerate(stats.view(-1)):
        #   cv2.rectangle(image, (offset, i * step),
        #                (offset + (data * maxLen), (i * step) + thicc), colors[i % 3], -1)
        return image


    if device.isOpened():  # try to get the first frame
        rval, frame = device.read()
    # print(frame.shape)
    else:
        rval = False
    out = torch.zeros(27)
    fps = 0

    commands = Commands.commands

    start = time()


    class pearsons(Enum):
        SD = "SD"
        JD = "JD"
        RD = "RD"
        AD = "AD"
        KH = "KH"


    ##settings
    add = False
    # if false all files in existing dir will be deleted
    saving = True
    command = commands.stopCommand
    pearson = pearsons.SD
    howMany = 100
    savePerSec = 5.0
    ##end settigns

    dir = r'D:\DataSetNew\{}\{}'.format(command.name, pearson.name)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    lenfile = dir + r'\len.txt'
    files = os.listdir(dir)
    file = 0
    if files:
        if add:
            F = open(lenfile, "r")
            file = int(F.read())
        else:
            for f in files:
                os.remove(os.path.join(dir, f))
    fullPath = dir + r'\{}_{}.jpg'
    savePerSec = 1 / savePerSec
    start = False
    if add:
        print("Adding files")
    else:
        print("Old files deleted")
    print("Creating dataset. Gesture: {}. Pearson: {}".format(command.name, pearson.name))
    while True:
        rval, frame = device.read()
        # print("time: {}".format(time()))
        if saving and start and time() - start > savePerSec:
            start = time()
            file += 1
            path = fullPath.format(command.value, file)
            print("saving file: {}".format(path))
            cv2.imwrite(path, frame)
            if file == howMany:
                break
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        frameWithStats = frame.copy()
        frame = frame[:, cut:width]
        frameWithStats = drawStatistics(frameWithStats, out, 1)
        cv2.imshow("processedImage", frame)
        cv2.imshow("AllImage", frameWithStats)
        key = cv2.waitKey(1)
        if key == 32:
            if start:
                break
            else:
                start = True

    F = open(lenfile, "w")
    F.write(str(file))
    print("saved {} files".format(file))
