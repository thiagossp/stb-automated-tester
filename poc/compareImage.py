from skimage.measure import structural_similarity as ssim
import numpy as np
import cv2

picture1 = cv2.imread('logos/frame245.jpg')
picture2 = cv2.imread('images/frame245.jpg')

##

histogram1 = cv2.calcHist([picture1], [0], None, [256], [0, 256])
histogram2 = cv2.calcHist([picture2], [0], None, [256], [0, 256])

c1, c2 = 0, 0

i = 0 
while i < len(histogram1) and i < len(histogram2):
    c1 += (histogram1[i] - histogram2[i])**2
    i += 1
c1 = c1**(1 / 2)
print(c1)
