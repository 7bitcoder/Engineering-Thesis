import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import glob
import re
import cv2
import numpy as np
import os
import random


class myDataset(Dataset):
    """hand symbols dataset."""

    def __init__(self, dir, split, test=False, train=False, validation=False, transform=None):
        """
            dir - directory to dataset
        """
        self.dir = dir
        self.transform = transform
        splitter = ""
        if test:
            splitter = '**/*0.jpg'
        elif train:
            splitter = '**/*[2-9].jpg'
        elif validation:
            splitter = '**/*1.jpg'
        else:
            raise Exception("chose one of train/test/validation")
        self.pathsList = glob.glob(self.dir + splitter, recursive=True)

    def __len__(self):
        return len(self.pathsList)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        path = self.pathsList[idx]
        image = cv2.imread(path)  # 480 x 640 x3
        gesture, fileNr = os.path.basename(path).split('_')
        nmb = int(gesture)
        label = np.zeros(13)
        label[nmb - 1] = 1
        if self.transform:
            image = cv2.flip(image, 1)
            image = image[:, 160:640]
            image = self.transform(image)
        return (image, torch.tensor(label, dtype=torch.float))


class KinectDataset(Dataset):
    """hand symbols dataset."""

    def __init__(self, dir, split, test=False, transform=None):
        """
            dir - directory to dataset
        """
        self.dir = dir
        self.transform = transform
        splitter = ""
        if (not test):
            splitter = '**/*[' + str(split) + '-9]_rgb.png'
        else:
            splitter = '**/*[0-' + str(split - 1) + ']_rgb.png'
        self.pathsList = glob.glob(self.dir + splitter, recursive=True)

    def __len__(self):
        return len(self.pathsList)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        path = self.pathsList[idx]
        image = cv2.imread(path)
        label = int(re.findall(r'G\d', path)[0][1:])
        label = np.eye(10)[label]
        if self.transform:
            image = self.transform(image)
        return (image, torch.tensor(label, dtype=torch.float))


class LaRED(Dataset):
    """hand symbols dataset."""

    def __init__(self, dir, split, test=False, transform=None):
        """
            dir - directory to dataset
        """
        self.dir = dir
        self.transform = transform
        splitter = ""
        if (not test):
            splitter = '**/O001/*[' + str(split + 1) + '-9].jpg'
        else:
            splitter = '**/O001/*[0-' + str(split) + '].jpg'
        self.pathsList = glob.glob(self.dir + splitter, recursive=True)

    def __len__(self):
        return len(self.pathsList)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        path = self.pathsList[idx]
        image = cv2.imread(path)
        nmb = int(re.findall(r'G\d\d\d', path)[0][1:])
        label = np.zeros(27)
        label[nmb] = 1
        if self.transform:
            image = self.transform(image)
        return (image, torch.tensor(label, dtype=torch.float))


if __name__ == "__main__":
    # test
    split = 2
    import openCvTranforms.opencv_transforms.transforms as tf

    heigh = 200
    width = 200


    def imshow(img):
        img = img[0].permute(1, 2, 0).numpy() / 2 + 0.5
        # img = img.view(heigh, width, 3).numpy()   # unnormalize
        print(img.shape)
        cv2.imshow("preview", img)


    transform = transforms.Compose([
        tf.myRandomCrop(380, 480),
        tf.Resize((heigh, width)),
        tf.ColorJitter(brightness=0.5, contrast=0.5),
        tf.ToTensor(),
        tf.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    dir = "D:/DataSetNew/"
    testDataset = myDataset(dir, split, test=True, transform=transform)
    trainDataset = myDataset(dir, split, test=False, transform=transform)
    lts = len(testDataset)
    ltr = len(trainDataset)
    print("test: {}, train {}".format(lts, ltr))
    print("sum : {}, check {}".format(ltr + lts, (ltr + lts) / 13))
    # for idx in range(len(dat)):
    #   print(dat.__getitem__(idx))

    testLoader = torch.utils.data.DataLoader(testDataset,
                                             batch_size=1, shuffle=False,
                                             num_workers=4)

    trainLoader = torch.utils.data.DataLoader(trainDataset,
                                              batch_size=1, shuffle=True,
                                              num_workers=4)

    for data in trainLoader:
        images, labels = data
        imshow(images)
        cv2.waitKey(0)
