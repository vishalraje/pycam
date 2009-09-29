#!/usr/bin/env python

# a simple edge detection filter

from pycam import VideoCapturePlayer
from pygame import surfarray
import numpy
from scipy import signal

laplacian_filter = numpy.array([[0,1,0],[1,-4,1],[0,1,0]])

def edgeDetect(surf):
    gray_image = numpy.mean(surfarray.array3d(surf), 2)
    
    edges = signal.convolve2d(gray_image, laplacian_filter, mode="same")
    
    surf = surfarray.make_surface(edges)
    return surf

     
if __name__ == '__main__':
    vcp = VideoCapturePlayer(processFunction=edgeDetect)
    vcp.main()
