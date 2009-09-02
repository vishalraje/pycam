# Load, Filter then Show an image with opencv in python
# Compile/Run with: python medianFilter.py

from opencv import cv
from opencv import highgui as hg

title = "Filtered Image"

a = hg.cvLoadImage('image.jpg')

b = cv.cvCreateMat(a.rows, a.cols, a.type)
filterSize = 3       # Must be odd
cv.cvSmooth(a, b, cv.CV_GAUSSIAN, filterSize)   # Carry out the filter operation

hg.cvNamedWindow(title)
hg.cvShowImage(title, b)               # Show the resulting image
hg.cvWaitKey()
hg.cvDestroyWindow(title)