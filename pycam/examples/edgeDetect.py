#!/usr/bin/env python
"""This example shows three methods of doing edge detection.
1) Using Pygame's inbuilt transform module
2) Using SciPy to convolve a 2 dimensional filter.
3) Using SciPy's cspline2d, and sepfir2d
"""
from pycam import VideoCapturePlayer
from pygame import surfarray
import numpy
from scipy import signal
from pygame import transform


# This decides which function to use
useScipy = False         # Otherwise use pygames inbuilt transform tools for the edge detection.
scipySpline = useScipy and False     # or laplacian filter...

   
def edgeDetectionProcess(surf):
    """This function takes a Pygame Surface detects edges in the image, and
    returns a pygame surface.
    
    """
    if useScipy:
        imageArray1 = numpy.mean(surfarray.array3d(surf),2) # converting here to one col
        if scipySpline:
            imageArray2 = edgeDetect2(imageArray1)
        else:
            imageArray2 = edgeDetect1(imageArray1)
        surf = surfarray.make_surface(imageArray2)
    else:
        # use pygame transform
        surf = transform.laplacian(surf)
    return surf

def edgeDetect1(imageArray):
    """Using the image assumed to have shape: (xx,yy,3)
    carry out some edge detection on the average of those colors.
    """
    # Create the filter
    laplacian = numpy.array([[0,1,0],[1,-4,1],[0,1,0]])
    
    # Convolve the filter with the array
    deriv = signal.convolve2d(
        imageArray
        ,laplacian,mode="same",boundary="symm")
    return deriv
     
def edgeDetect2(imageArray):
    derfilt = numpy.array([1.0,-2,1.0],numpy.float32)
    ck = signal.cspline2d(imageArray,8.0)
    deriv = signal.sepfir2d(ck, derfilt, [1]) + signal.sepfir2d(ck, [1], derfilt)
    return deriv
     

def main():
    vcp = VideoCapturePlayer(processFunction=edgeDetectionProcess)
    vcp.main()


if __name__ == '__main__':
    main()
