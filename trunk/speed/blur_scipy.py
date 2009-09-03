#!/usr/bin/env python
"""
Show an image and filter with scipy in python
Brian Thorne - July 09
Compile/Run with: python blur_scipy.py
"""

from __future__ import division
from numpy import array, uint8
from scipy import signal, ndimage
from VideoCapturePlayer import VideoCapturePlayer as VCP
from misc import scipyFromOpenCV

def opencvFilt2sigma(size):
    """OpenCV defaults to making sigma up with this formula.
    Learning OpenCV: computer vision with the OpenCV library
    By Gary Bradski, Adrian Kaehler pg 112"""
    return (( size/2 ) - 1)*0.30 + 0.80

@scipyFromOpenCV
def gaussianBlur(np_image):
    """Blur an image with scipy"""
    filterSize = opencvFilt2sigma(43)
    result = ndimage.filters.gaussian_filter(np_image, 
                            (filterSize, filterSize, 1))
    return result

def main():
    title = "Guassian Filtered Output"
    VCP(gaussianBlur,title=title).main()

if __name__ == "__main__": 
    main()
    #import cProfile
    #cProfile.run("main()",'python_profile_data')

