#!/usr/bin/env python

"""
Load, Calculate the harris response then Show an image with opencv in python
Brian Thorne 2009
"""

from VideoCapturePlayer import VideoCapturePlayer as VCP
import numpy

from opencv import cv
from IPython.Shell import IPShellEmbed
from harris import filter_and_render_cv


def harrisResponse(image):
    """pyvision/point/DetectorHarris.py
    Runs at 10.5 fps...
    """
    gray = cv.cvCreateImage( cv.cvGetSize(image), 8, 1 )
    corners = cv.cvCreateImage( cv.cvGetSize(image), 32, 1 )
    cv.cvCvtColor( image, gray, cv.CV_BGR2GRAY )

    cv.cvCornerHarris(gray,corners,25)
    
    image = filter_and_render_cv(image,corners)
    
    return image
    

    

if __name__ == "__main__":
    title = "Harris Feature Detection"
    VCP(harrisResponse, title).main()
