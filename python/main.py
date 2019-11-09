from __future__ import print_function
import numpy as np
import torch
from torchvision import transforms, datasets

x = torch.tensor([[1,2,3,4,5],[6,7,8,1,2]], dtype=torch.long);
y = torch.full_like(x,5);
print(torch.cuda.is_available())
print(x.view([1,-1]))

train = datasets.MNIST("", train= True, download= True,
                       transform= transforms.Compose([transforms.ToTensor()]))


test = datasets.MNIST("", train= False, download= True,
                       transform= transforms.Compose([transforms.ToTensor()]))
 trainset =  train.