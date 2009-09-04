#!/usr/bin/env python

"""
Load, Filter then Show an image with opencv in python
Brian Thorne 2009
"""

from VideoCapturePlayer import VideoCapturePlayer as VCP
from opencv import cv

def medianBlur(image, filterSize=43):
    """Blur an image with a particular strength filter."""
    cv.cvSmooth(image, image, cv.CV_MEDIAN, filterSize)
    return image

if __name__ == "__main__":
    title = "Median Filtered Output"
    VCP(medianBlur, title).main()
