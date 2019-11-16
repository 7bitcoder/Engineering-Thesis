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

if torch.cuda.is_available():
    device = torch.device("cuda:0")  # you can continue going on here, like cuda:1 cuda:2....etc.
    print("Running on the GPU")
else:
    device = torch.device("cpu")
    print("Running on the CPU")

split = 2
size = 256

transform = transforms.Compose(
    [tf.Resize((size, size)),
     tf.Grayscale(),
     tf.ToTensor(),
     tf.Normalize((0.5,), (0.5,))])

test = KinectDataset("kinect_leap_dataset/", split, test=True, transform=transform)
train = KinectDataset("kinect_leap_dataset/", split, test=False, transform=transform)
print(len(test))
print(len(train))

testDataset = torch.utils.data.DataLoader(test,
                                          batch_size=4, shuffle=False)

trainDataset = torch.utils.data.DataLoader(train,
                                           batch_size=4, shuffle=True)

print(len(testDataset))
print(len(trainDataset))


# plot image with opencv
def imshow(img):
    img = img / 2 + 0.5  # unnormalize
    npimg = img.numpy()
    cv2.imshow(np.transpose(npimg, (1, 2, 0)))


MODEL_NAME = f"model-{int(time.time())}"  # gives a dynamic model name, to just help with things getting messy over time.
net = Net(size).to(device)
optimizer = optim.Adam(net.parameters(), lr=0.001)
loss_function = nn.MSELoss()

print("Model name: " + MODEL_NAME)


def test(length=32):
    for i, data in enumerate(testDataset, len(testDataset) - length):
        image, label = data
        val_acc, val_loss = fwd_pass(image.view(-1, 1, size, size).to(device), label.to(device))
    return val_acc, val_loss


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


def train(net):
    BATCH_SIZE = 100
    EPOCHS = 2

    with open("model.log", "w") as f:
        for epoch in range(EPOCHS):
            print("epoch: " + str(epoch))
            running_loss = 0.0
            i = 0
            t = tqdm(total=len(trainDataset))  # Initialise
            for data in trainDataset:
                t.update(1)
                images, labels = data
                images = images.view(-1, 1, size, size)
                images, labels = images.to(device), labels.to(device)

                acc, loss = fwd_pass(images, labels, train=True)

                # print(f"Acc: {round(float(acc),2)}  Loss: {round(float(loss),4)}")
                # f.write(f"{MODEL_NAME},{round(time.time(),3)},train,{round(float(acc),2)},{round(float(loss),4)}\n")
                # just to show the above working, and then get out:
                if i % 51 == 50:
                    val_acc, val_loss = test(length=100)
                    #print(val_acc, float(val_loss))
                    f.write(
                        f"{MODEL_NAME},{round(time.time(), 3)},{round(float(acc), 3},{round(float(loss), 4)},{round(float(val_acc), 3)},{round(float(val_loss), 4)},{epoch}\n")
                i += 1
            t.close()


train(net)
