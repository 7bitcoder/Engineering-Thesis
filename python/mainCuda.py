import numpy as np
from tqdm import tqdm
import torch
import torch.optim as optim
import time
from neuralNetwork import Net
import torch.nn as nn
from datasetLoader import *
import openCvTranforms.opencv_transforms.transforms as tf
import torchvision.transforms as transforms
import keyboard


# plot image with opencv
def imshow(img):
    img = img / 2 + 0.5  # unnormalize
    npimg = img.numpy()
    cv2.imshow(np.transpose(npimg, (1, 2, 0)))


def test(length=32):
    val_acc = val_loss = 0
    for i, data in enumerate(testDataset):
        image, label = data
        out = fwd_pass(image.view(-1, 3, heigh, width).to(device), label.to(device))
        val_acc += out[0]
        val_loss += out[1]
        if i == length:
            break
    return val_acc / length, val_loss / length


def fwd_pass(images, labels, train=False):
    if train:
        net.zero_grad()
    outputs = net(images)
    acc = 0
    length = len(labels)

    matches = [torch.argmax(i) == torch.argmax(j) for i, j in zip(outputs, labels)]
    acc = matches.count(True) / len(matches)

    loss = loss_function(outputs, labels)

    if train:
        loss.backward()
        optimizer.step()
    return acc, loss


def train(net, epochs, startingEpoch):
    EPOCHS = epochs
    # if it is already trained
    if startEpoch > epochs:
        return epochs + 1

    with open(logFile, "a") as f:
        for epoch in range(startingEpoch, EPOCHS):
            print("\aepoch: " + str(epoch))
            running_loss = 0.0
            i = 0
            exit = False
            t = tqdm(total=len(trainDataset))  # Initialise
            for data in trainDataset:

                if keyboard.is_pressed('q'):  # exit on ESC
                    exit = True
                    print('\aAfter this epoch training will end')
                t.update(1)
                images, labels = data
                images = images.view(-1, 3, heigh, width)
                images, labels = images.to(device), labels.to(device)

                acc, loss = fwd_pass(images, labels, train=True)

                if i % 80 == 79:
                    val_acc, val_loss = test(64)
                    # print(val_acc, float(val_loss))
                    f.write(
                        f"{MODEL_NAME},{round(time.time(), 3)},{round(float(acc), 3)}, {round(float(loss), 4)}, {round(float(val_acc), 3)}, {round(float(val_loss), 4)}, {epoch}\n")
                i += 1
            t.close()
            if exit:
                return epoch + 1
        return epochs + 1


class globNr(object):
    nr = 19


if __name__ == "__main__":
    if torch.cuda.is_available():
        device = torch.device("cuda:0")  # you can continue going on here, like cuda:1 cuda:2....etc.
        print('Available gpu\'s: ' + str(torch.cuda.device_count()))
        print("Running on the GPU")
    else:
        device = torch.device("cpu")
        print("Running on the CPU")
    # split data to test/train 0-9
    nr = globNr.nr
    trainStateFilename = "./savedTrainState{}.pth".format(nr)
    modelFilename = "./savedMode{}.pth".format(nr)
    dataSetPath = "D:/DataSetNew/"
    logFile = 'model{}.log'.format(nr)
    loadTrainData = True
    split = 1
    width = 60
    heigh = 60
    epochs = 10
    batchSize = 15
    startEpoch = 0

    transform = transforms.Compose(
        [tf.Resize((heigh, width)),
         tf.ToTensor(),
         tf.Normalize((0.5,), (0.5,))])

    testLoader = myDataset(dataSetPath, split, test=True, transform=transform)
    trainLoader = myDataset(dataSetPath, split, test=False, transform=transform)
    print("test {}, train {}".format(len(testLoader), len(trainLoader)))
    testDataset = torch.utils.data.DataLoader(testLoader,
                                              batch_size=batchSize, shuffle=True)

    trainDataset = torch.utils.data.DataLoader(trainLoader,
                                               batch_size=batchSize, shuffle=True)

    net = Net(width, heigh).to(device)
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    if loadTrainData:
        print('Loading saved Training State')
        state = torch.load(trainStateFilename)
        if [split, width, heigh] != [state['split'], state['width'], state['height']]:
            raise Exception('Load Training data differ from actual')
        startEpoch = state['startEpoch']
        logFile = state['logFile']
        batchSize = state['batchSize']
        net.load_state_dict(state['state_dict'])
        optimizer.load_state_dict(state['optimizer'])
        print('Data loaded: starting epoch: ' + str(startEpoch) + ' log File: ' + str(logFile) + ' batch size: ' + str(
            batchSize))
    loss_function = nn.MSELoss()
    MODEL_NAME = f"model-{int(time.time())}"  # gives a dynamic model name, to just help with things getting messy over time.
    print("Model name: " + MODEL_NAME)
    print("test dataset size: " + str(len(testDataset)) + " train dataset size: " + str(len(trainDataset)))
    startEpoch = train(net, epochs, startEpoch)
    state = {
        'logFile': logFile,
        'epoch': epochs,
        'startEpoch': startEpoch,
        'split': split,
        'width': width,
        'height': heigh,
        'batchSize': batchSize,
        'state_dict': net.state_dict(),
        'optimizer': optimizer.state_dict(),
    }
    torch.save(state, trainStateFilename)
    net.to("cpu")
    torch.save(net, modelFilename)
