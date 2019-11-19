import shutil
import os

dir = 'laRED_dataset/M005'
chosen = [1, 4, 6, 8, 14, 19, 20, 22, 25, 26]
list = os.listdir(dir)
print(list)
for x in list:
    if not int(x[1:]) in chosen:
        print(x)
        shutil.rmtree(os.path.join(dir, x))
