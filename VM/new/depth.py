import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

I1 = cv.imread('r1.png')
I2 = cv.imread('r2.png')

A = plt.stereoAnaglyph(I1,I2)
plt.imshow(A)

# imgL = cv.imread('r1.png',0)
# imgR = cv.imread('r2.png',0)
# stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
# disparity = stereo.compute(imgL,imgR)
# plt.imshow(disparity,'gray')
# plt.show()