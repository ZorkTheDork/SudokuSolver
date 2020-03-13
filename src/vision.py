import imutils
import cv2
from matplotlib import pyplot as plt
import numpy as np

image = cv2.imread("./test.jpg")

grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(grey, (5, 5), 0)
edged = cv2.Canny(blurred, 90, 150, apertureSize=3)
kernel = np.ones((3, 3), np.uint8)
dialated = cv2.dilate(edged, kernel, iterations=1)

plt.imshow(dialated, cmap='gray')
plt.show()