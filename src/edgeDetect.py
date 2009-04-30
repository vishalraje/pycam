#!/usr/bin/env python

# TODO Third option for edge detect - use opencv

import pygame
from VideoCapturePlayer import *

from pygame import surfarray
import numpy
from scipy import signal
from pygame import transform

useOpenCvCam = True
edgeDetection = True
useScipy = False         # Otherwise use pygames inbuilt transform tools for the edge detection.
scipySpline = useScipy and True     # or laplacian filter...


if useOpenCvCam:
    # We want to raise an exception as soon as possible if no opencv found when required
    import opencv
    
def edgeDetectionProcess(surf):
    if useScipy:
        imageArray1 = numpy.mean(surfarray.pixels3d(surf),2) # converting here to one col
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
    carry out some edge detection on the average of those colors. Could prolly use a conversion to gray...
    """
    laplacian = numpy.array([[0,1,0],[1,-4,1],[0,1,0]])
    deriv = signal.convolve2d(
        imageArray[:,:]
        ,laplacian,mode="same",boundary="symm")
    return deriv
     
def edgeDetect2(imageArray):
    derfilt = numpy.array([1.0,-2,1.0],numpy.float32)
    ck = signal.cspline2d(imageArray[:,:],8.0)
    deriv = signal.sepfir2d(ck, derfilt, [1]) + signal.sepfir2d(ck, [1], derfilt)
    return deriv
     

def main():
    vcp = VideoCapturePlayer(processFunction=edgeDetectionProcess)
    vcp.main()
    pygame.quit()

if __name__ == '__main__':
    main()
