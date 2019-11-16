import torch
from torch.utils.data import Dataset, DataLoader
import glob
import re
import cv2


class KinectDataset(Dataset):
    """hand symbols dataset."""

    def __init__(self, dir, transform=None):
        """
            dir - directory to dataset
        """
        self.dir = dir
        self.transform = transform
        self.pathsList = glob.glob(self.dir + '**/*_rgb.png', recursive=True)
        self.mathLabel = p = re.compile(r'(G[0-9]+)')
        print(self.pathsList)

    def __len__(self):
        return len(self.pathsList)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        path = self.pathsList[idx]
        image = cv2.imread(path)
        label = int(re.findall(r'G\d+', path)[0][1:])
        data = {'image': image, 'label': label}
        if self.transform:
            data = self.transform(data)
        return data


if __name__ == "__main__":
    dat = KinectDataset("kinect_leap_dataset/")
    for idx in range(len(dat)):
        print(dat.__getitem__(idx))