#!/usr/bin/env python

from pycam import VideoCapturePlayer, numpyFromSurf
from scipy.ndimage import morphology

@numpyFromSurf
def dilate(image):
    return image
    #return morphology.grey_dilation(image,(10,10,1) )

if __name__ == '__main__':
    vcp = VideoCapturePlayer(processFunction=dilate)
    vcp.main()
