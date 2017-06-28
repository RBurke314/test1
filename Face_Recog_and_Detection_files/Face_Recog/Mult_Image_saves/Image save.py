import numpy as np
import cv2

capture1 = cv2.VideoCapture(0)
capture2 = cv2.VideoCapture(1)

for fn in range(0, 10):
    print 'processing %s...' % fn,
    ret1, imgL = capture1.read()
    ret2, imgR = capture2.read()
    cv2.imwrite("Leftimage%s.png" % fn, imgL)
    cv2.imwrite("Rightimage%s.png" % fn, imgR)
