#!/usr/bin/env python

"""
Load, Filter then Show an image with opencv in python
Brian Thorne 2009
"""

from VideoCapturePlayer import VideoCapturePlayer as VCP

from opencv import cv


def gaussianBlur(image):
    """Blur an image"""
    result = cv.cvCreateMat(image.rows, image.cols, image.type)
    filterSize = 43 #139 gives a very strong blur, but takes a while
    cv.cvSmooth(image, result, cv.CV_GAUSSIAN, filterSize)   # Carry out the filter operation
    return result

if __name__ == "__main__":
    title = "Guassian Filtered Output"
    vcp = VCP(gaussianBlur, title)
    vcp.main()
