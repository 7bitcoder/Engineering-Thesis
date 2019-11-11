import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(2)
print(vc.get(5))
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    print(frame.shape)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")