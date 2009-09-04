#!/usr/bin/env python

"""
Load, Filter then Show an image with opencv in python
Brian Thorne 2009
"""

from VideoCapturePlayer import VideoCapturePlayer as VCP

from opencv import cv
from misc import opencvFilt2sigma

def gaussianBlur(image, filterSize=43, sigma=opencvFilt2sigma(43)):
    """Blur an image with a particular strength filter.
    Default is 43, 139 gives a very strong blur, but takes a while
    """
    
    # Carry out the filter operation
    cv.cvSmooth(image, image, cv.CV_GAUSSIAN, filterSize, 0, sigma)
    return image

if __name__ == "__main__":
    title = "Guassian Filtered Output"
    VCP(gaussianBlur, title).main()
