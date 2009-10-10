#!/usr/bin/env python

from VideoCapturePlayer import VideoCapturePlayer as VCP
from opencv import cv

def dilateImage(image):
    cv.cvDilate(image, image, None, 5)
    return image

if __name__ == "__main__":
    VCP(dilateImage, "Dilated Image").main()
