import torch.nn.functional as F
import torch.nn as nn
import torch


class Net2(nn.Module):
    def __init__(self, width, heigh):
        super(Net2, self).__init__()

        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)

        # todo remember to update when network structure is changed

        # calculate entrance to linear
        # convolution
        width -= 4
        heigh -= 4
        # pool
        width /= 2
        heigh /= 2
        # convolution
        width -= 4
        heigh -= 4
        # pool
        width /= 2
        heigh /= 2
        self.linearInput = 16 * int(width) * int(heigh);
        self.fc1 = nn.Linear(self.linearInput, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, self.linearInput)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Net(nn.Module):
    def __init__(self, width, heigh):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 4, 5)
        self.conv2 = nn.Conv2d(4, 8, 5)
        #self.conv3 = nn.Conv2d(32, 64, 5)

        # calculate entrance to linear
        # convolution
        width -= 4
        heigh -= 4
        # pool
        width /= 2
        heigh /= 2
        # convolution
        width -= 4
        heigh -= 4
        # pool
        width /= 2
        heigh /= 2
        # convolution
        #width -= 4
        #heigh -= 4
        # pool
        #width /= 2
        #heigh /= 2
        self.linearInput = 8 * int(width) * int(heigh)

        self.fc1 = nn.Linear(self.linearInput, 13)
        self.fc2 = nn.Linear(13, 13)

    def convs(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = F.max_pool2d(x, (2, 2))
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, (2, 2))
        #x = self.conv3(x)
        #x = F.relu(x)
        #x = F.max_pool2d(x, (2, 2))
        return x

    def forward(self, x):
        x = self.convs(x)
        x = x.view(-1, self.linearInput)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)
