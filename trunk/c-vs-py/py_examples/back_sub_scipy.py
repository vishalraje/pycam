#!/usr/bin/env python
"""
~7fps
Brian Thorne - September 09

"""

from __future__ import division
import numpy as np
from numpy import array, uint8
from scipy import signal, ndimage
from VideoCapturePlayer import VideoCapturePlayer as VCP
from misc import scipyFromOpenCV, opencvFilt2sigma

from IPython.Shell import IPShellEmbed
from scipy.ndimage import morphology


@scipyFromOpenCV
def threshold_image(np_image, n=[]):
    """Record the first 5 images to get a background, then diff current frame with the last saved frame.
    """
    if len(n) < 5:
        # n[4] will be our background
        # First capture a few images
        n.append(np_image[:])
        if len(n) == 5:
            # last time here 
            #n[4] = ndimage.filters.gaussian_filter(n[4],3,order=0)
            pass 
        return np_image
    original = n[4]
    img = np_image[:]
    
    
    
    differenceImage = abs(np_image.astype(float) - original.astype(float)).astype(uint8)
    # filter out random noise
    #differenceImage = ndimage.median_filter(differenceImage,size=3)
    
    """The threshold value determines the amount of "Change" required 
    before something will show up"""
    thresholdValue = 30
    # Take the N-Dimensional difference (3 channels of binary)
    differenceImage = (differenceImage >= thresholdValue)
    
    # Convert this to one channel binary
    differenceImage = differenceImage.mean(2).astype(bool)
    
    # Smooth the edges of the mask
    #differenceImage = ndimage.filters.gaussian_filter(differenceImage,0.5) 
    
    # Remove Salt & Pepper Noise
    differenceImage = ndimage.median_filter(differenceImage,size=5)
    
    
    #IPShellEmbed()()
    output = np.zeros(img.shape).astype(img.dtype)
    output[differenceImage] = img[differenceImage]
    return output



def main():
    title = "SciPy Background Subtraction"
    
    VCP(threshold_image,title=title).main()
    

if __name__ == "__main__": 
    #testGaussianBlur()
    main()
    #import cProfile
    #cProfile.run("main()",'python_profile_data')

