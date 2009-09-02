#!/usr/bin/env python
"""
Show an image and filter with scipy in python
Brian Thorne - July 09
Compile/Run with: python blur_scipy.py
"""


from numpy import array, uint8
from scipy import signal, ndimage

from VideoCapturePlayer import VideoCapturePlayer as VCP


from misc import scipyFromOpenCV

@scipyFromOpenCV
def gaussianBlur(np_image):
    """Blur an image with scipy"""
    filterSize = 13     #139 gives a very strong blur, but takes a while
    result = ndimage.filters.gaussian_filter(np_image, (filterSize, filterSize, 1))
    return result


from misc import gauss_kern

@scipyFromOpenCV
def slowGaussianBlur(matrix):
    """Manual gaussian blur - Very very very slow!"""
    filterSize = 3
    filt = gauss_kern(filterSize)

    r = signal.convolve(matrix[:,:,0],filt,'same')
    g = signal.convolve(matrix[:,:,1],filt,'same')
    b = signal.convolve(matrix[:,:,2],filt,'same')
    
    result = array([r,b,g]).astype(uint8).transpose((1,2,0))
   
    return result


def main():
    title = "Guassian Filtered Output"
    vcp = VCP(gaussianBlur,title=title)
    #vcp = VCP(slowGaussianBlur,title=title)
    vcp.main()

if __name__ == "__main__": 
    main()
    #import cProfile
    #cProfile.run("main()",'python_profile_data')

