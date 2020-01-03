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
import copy

if torch.cuda.is_available():
    device = torch.device("cuda:0")  # you can continue going on here, like cuda:1 cuda:2....etc.
    print('Available gpu\'s: ' + str(torch.cuda.device_count()))
    print("Running on the GPU")
else:
    print("Running on the CPU")
device = torch.device("cpu")


def train_model(model, dataloaders, criterion, optimizer, num_epochs=25, is_inception=False):
    since = time.time()

    val_acc_history = []

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()  # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    # Get model outputs and calculate loss
                    # Special case for inception because in training it has an auxiliary output. In train
                    #   mode we calculate the loss by summing the final output and the auxiliary output
                    #   but in testing we only consider the final output.
                    if is_inception and phase == 'train':
                        # From https://discuss.pytorch.org/t/how-to-optimize-inception-model-with-auxiliary-classifiers/7958
                        outputs, aux_outputs = model(inputs)
                        loss1 = criterion(outputs, labels)
                        loss2 = criterion(aux_outputs, labels)
                        loss = loss1 + 0.4 * loss2
                    else:
                        outputs = model(inputs)
                        loss = criterion(outputs, labels)

                    _, preds = torch.max(outputs, 1)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
            if phase == 'val':
                val_acc_history.append(epoch_acc)

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, val_acc_history


if __name__ == "__main__":
    # split data to test/train 0-9
    nr = 6
    trainStateFilename = "./savedTrainState{}.pth".format(nr)
    modelFilename = "./savedMode{}.pth".format(nr)
    dataSetPath = "D:/DataSetNew/"
    logFile = 'model{}.log'.format(nr)
    loadTrainData = False
    split = 1
    width = 60
    heigh = 60
    epochs = 30
    batchSize = 15
    startEpoch = 0
    image_datasets = []

    transform = transforms.Compose([
        tf.Resize((224, 224)),
        tf.ToTensor(),
        tf.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image_datasets = {
        'val': myDataset(dataSetPath, split, test=True, transform=transform),
        'train': myDataset(dataSetPath, split, test=False, transform=transform)
    }
    print("train {}, val {}".format(len(image_datasets['train']), len(image_datasets['val'])))
    dataloaders_dict = {
        x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batchSize, shuffle=True, num_workers=1) for x in
        ['train', 'val']}

    # net = Net(width, heigh).to(device)
    ###
    net = torch.hub.load('pytorch/vision:v0.4.2', 'resnet18', pretrained=True).to(device)
    # model.eval()

    num_ftrs = net.fc.in_features
    net.fc = nn.Linear(num_ftrs, 13)

    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    criterion = nn.CrossEntropyLoss()

    model_ft, hist = train_model(net, dataloaders_dict, criterion, optimizer, num_epochs=30)

    if loadTrainData:
        print('Loading saved Training State')
        state = torch.load(trainStateFilename)
        if [epochs, split, width, heigh] != [state['epoch'], state['split'], state['width'], state['height']]:
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
    model_ft, hist = train_model(net, dataloaders_dict, criterion, optimizer, num_epochs=30)
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
