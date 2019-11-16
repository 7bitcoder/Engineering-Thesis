import torch
from torchvision import transforms, utils


class Rescale(object):
    """Rescale image to given size must me touple or int.
    """

    def __init__(self, outSize):
        assert isinstance(outSize, (int, tuple))
        self.size = outSize

    def __call__(self, data):
        image, landmarks = data['image'], data['label']
        height, width, channels = image.shape
        if isinstance(self.size, int):
            if height > width:
                new_height, new_width = self.size * h / w, self.output_size
            else:
                new_h, new_w = self.output_size, self.output_size * w / h
        else:
            new_h, new_w = self.output_size

        new_h, new_w = int(new_h), int(new_w)

        img = transform.resize(image, (new_h, new_w))

        # h and w are swapped for landmarks because for images,
        # x and y axes are axis 1 and 0 respectively
        landmarks = landmarks * [new_w / w, new_h / h]

        return {'image': img, 'landmarks': landmarks}


class RandomCrop(object):
    """Crop randomly the image in a sample.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        if isinstance(output_size, int):
            self.output_size = (output_size, output_size)
        else:
            assert len(output_size) == 2
            self.output_size = output_size

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        h, w = image.shape[:2]
        new_h, new_w = self.output_size

        top = np.random.randint(0, h - new_h)
        left = np.random.randint(0, w - new_w)

        image = image[top: top + new_h,
                      left: left + new_w]

        landmarks = landmarks - [left, top]

        return {'image': image, 'landmarks': landmarks}


class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        image = image.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image),
                'landmarks': torch.from_numpy(landmarks)}


def transformData():
    import os
    import glob
    import re
    import copy
    splitter = r'kinect_leap_dataset/**/10_rgb*'
    pathsList = glob.glob(splitter, recursive=True)
    for path in pathsList:
        old = copy.deepcopy(path)
        ten = '10'
        new = (path[::-1].replace(ten[::-1], '0', 1))[::-1]
        print(new)
        os.rename(old,new)