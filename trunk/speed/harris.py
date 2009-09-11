"""

Shared code for harris feature detector

"""

from opencv import adaptors
import numpy
from numpy import array,ones,zeros,nonzero
from scipy.ndimage import gaussian_filter,maximum_filter
from opencv import cv


def filter_and_render_cv(image, response):
    """
    Takes a cvMat image and response, filters for interesting points
    that are a min dist apart.
    """  
    corners = response
    buffer = corners.imageData
    corners = numpy.frombuffer(buffer,numpy.float32).reshape(corners.height,corners.width).transpose()
    #IPShellEmbed()()
    i = filter_and_render_mixed(image, corners)
    return i

def filter_and_render_numpy(image, response):
    """Take a numpy image and response"""
    i = adaptors.NumPy2Ipl(image)
    return filter_and_render_mixed(i, response.T)

def filter_and_render_mixed(image, corners):
    """
    Takes a numpy array of corners and a cvMat image.
    
    """
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
