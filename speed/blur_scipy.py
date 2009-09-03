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

def main():
    title = "Guassian Filtered Output"
    VCP(gaussianBlur,title=title).main()

if __name__ == "__main__": 
    main()
    #import cProfile
    #cProfile.run("main()",'python_profile_data')

