#!/usr/bin/env python

"""
Load, Filter then Show an image with opencv in python
Brian Thorne 2009
"""

from VideoCapturePlayer import VideoCapturePlayer as VCP
import numpy
from scipy.ndimage import gaussian_filter,maximum_filter
from numpy import array,ones,zeros,nonzero
from opencv import cv


def harrisResponse(image):
    """pyvision/point/DetectorHarris.py
    Runs at 10.5 fps...
    """
    gray = cv.cvCreateImage( cv.cvGetSize(image), 8, 1 )
    corners = cv.cvCreateImage( cv.cvGetSize(image), 32, 1 )
    cv.cvCvtColor( image, gray, cv.CV_BGR2GRAY )

    cv.cvCornerHarris(gray,corners,15)
    
    # Filter the response and draw points
    buffer = corners.imageData
    corners = numpy.frombuffer(buffer,numpy.float32).reshape(corners.height,corners.width).transpose()
    n = 15
    footprint = ones((n,n))
    mx = maximum_filter(corners, footprint = footprint)
    local_maxima = (corners == mx) * (corners != zeros(corners.shape)) # make sure to remove completly dark points

    points = nonzero(local_maxima)
    del local_maxima

    points = array([points[0],points[1]]).transpose()
    L = []
    
    for each in points:
        L.append((corners[each[0],each[1]],each[0],each[1],None))
        i = cv.cvPoint(int(each[0]),int(each[1]))
        cv.cvCircle(image, i, 2, cv.CV_RGB(0,0,200),3 )
    
    #cv.cvCvtColor(grayimage, image, cv.CV_GRAY2RGB)
    return image

if __name__ == "__main__":
    title = "Harris Feature Detection"
    VCP(harrisResponse, title).main()
