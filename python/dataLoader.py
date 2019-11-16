import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import glob
import re
import cv2

class KinectDataset(Dataset):
    """hand symbols dataset."""

    def __init__(self, dir, split, test=False, transform=None):
        """
            dir - directory to dataset
        """
        self.dir = dir
        self.transform = transform
        splitter = ""
        if(not test):
            splitter = '**/*[' + str(split) + '-9]_rgb.png'
        else:
            splitter = '**/*[0-' + str(split-1) + ']_rgb.png'
        self.pathsList = glob.glob(self.dir + splitter, recursive=True)
        print(self.pathsList)

    def __len__(self):
        return len(self.pathsList)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        path = self.pathsList[idx]
        image = cv2.imread(path)
        label = int(re.findall(r'G\d', path)[0][1:])
        if self.transform:
            image = self.transform(image)
        return (image, label)


if __name__ == "__main__":
    #test
    split = 2
    transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.ToTensor(),
         transforms.Normalize((0.5,), (0.5,))])

    testDataset = KinectDataset("kinect_leap_dataset/", split, test=True, transform=transform)
    trainDataset = KinectDataset("kinect_leap_dataset/", split, test=False, transform=transform)
    print(len(testDataset))
    print(len(trainDataset))
    #for idx in range(len(dat)):
     #   print(dat.__getitem__(idx))


    testLoader = torch.utils.data.DataLoader(testDataset,
                                                 batch_size=4, shuffle=True,
                                                 num_workers=4)

    trainLoader = torch.utils.data.DataLoader(trainDataset,
                                                 batch_size=4, shuffle=True,
                                                 num_workers=4)

    dataiter = iter(testLoader)
    image, label = dataiter.next()
    print(image)
    print(label)