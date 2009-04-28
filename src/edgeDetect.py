#!/usr/bin/env python

import pygame
from VideoCapturePlayer import *

from pygame import surfarray
import numpy
from scipy import signal
from pygame import transform

useOpenCvCam = True
edgeDetection = True
useScipy = False         # Otherwise use pygames inbuilt transform tools.
scipySpline = useScipy and True     # or laplacian filter...

""" performance of get and process image: shows that it makes very little
opencv      edgeDetection       scipy       spline      result
true        false               N/A         N/A          66ms
false       false               n/A         n/a          66ms 
true        true                false       N/A          209ms  // opencv capture, pygame edge detection
false       true                false       n/a          211ms
true        true                true        false        553ms
false       true                true        false        551ms
true        true                true        true         790ms
false       true                true        true         795ms

"""

if useOpenCvCam:
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
