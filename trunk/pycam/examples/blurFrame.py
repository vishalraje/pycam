#!/usr/bin/python
"""

Usage:
    >>> 
   



"""

from pycam import VideoCapturePlayer

from pygame import surfarray
#import numpy
from scipy import signal, ndimage



def gaussianBlur(imageArray):
    """This function takes a pygame surface, converts it to a numpy array
    carries out gaussian blur, converts back then returns the pygame surface.
    """
    # Convert to a NumPy array.
    # In theory this should be able to be surfarray.pixels3d fro direct access.
    np_array = surfarray.array3d(imageArray)
    
    # The strength of the blur.
    sigma = 3
    
    # Filter the image
    result = ndimage.filters.gaussian_filter(np_array, 
                            sigma=(sigma, sigma, 0),
                            order=0,
                            mode='reflect'
                            )
    # Convert back to a surface.          
    surf = surfarray.make_surface(result)
    return surf
     

def main():

    vcp = VideoCapturePlayer(processFunction=gaussianBlur)
    vcp.main()


if __name__ == '__main__':
    main()
