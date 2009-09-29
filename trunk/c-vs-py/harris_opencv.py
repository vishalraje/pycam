#!/usr/bin/env python

"""
Load, Calculate the harris response then Show an image with opencv in python
Brian Thorne 2009
"""

from VideoCapturePlayer import VideoCapturePlayer as VCP
import numpy

from opencv import cv, highgui
from IPython.Shell import IPShellEmbed
from harris import filter_and_render_cv


def harrisResponse(image):
    """pyvision/point/DetectorHarris.py
    Runs at 10.5 fps...
    """
    gray = cv.cvCreateImage( cv.cvGetSize(image), 8, 1 )
    corners = cv.cvCreateImage( cv.cvGetSize(image), 32, 1 )
    cv.cvCvtColor( image, gray, cv.CV_BGR2GRAY )

    cv.cvCornerHarris(gray,corners,3)
    
    image = filter_and_render_cv(image,corners)
    #IPShellEmbed()()
    return image
    
def static_test():
    image_filename = "/usr/share/doc/opencv-doc/examples/c/lena.jpg"
    i = highgui.cvLoadImage(image_filename)
    result = harrisResponse(i)
    highgui.cvSaveImage("harris_response_lena_opencv.jpg", result)
    return result

if __name__ == "__main__":
    static_test()
    
    
    title = "Harris Feature Detection"
    VCP(harrisResponse, title).main()
