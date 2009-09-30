#!/usr/bin/env python
"""
Show an image and detect harris features with scipy in python.

Original source from:
http://jesolem.blogspot.com/2009/01/harris-corner-detector-in-python.html

Brian Thorne - July 09 - <brian.thorne@hitlabnz.org>

Compile/Run with: python harris_scipy.py
"""

from __future__ import division
import numpy as np
from pylab import *
from numpy import array, uint8
from scipy import signal, ndimage, misc
from VideoCapturePlayer import VideoCapturePlayer as VCP
from misc import scipyFromOpenCV, opencvFilt2sigma, gauss_kern
from IPython.Shell import IPShellEmbed
from opencv import adaptors
from harris import filter_and_render_numpy

from opencv import cv


def gauss_derivative_kernels(size, sizey=None):
    """ returns x and y derivatives of a 2D 
        gauss kernel array for convolutions """
    size = int(size)
    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)
    y, x = mgrid[-size:size+1, -sizey:sizey+1]

    #x and y derivatives of a 2D gaussian with standard dev half of size
    # (ignore scale factor)
    gx = - x * exp(-(x**2/float((0.5*size)**2)+y**2/float((0.5*sizey)**2))) 
    gy = - y * exp(-(x**2/float((0.5*size)**2)+y**2/float((0.5*sizey)**2))) 

    return gx,gy

def gauss_derivatives(im, n, ny=None):
    """ returns x and y derivatives of an image using gaussian 
        derivative filters of size n. The optional argument 
        ny allows for a different size in the y direction."""
    
    gx,gy = gauss_derivative_kernels(n, sizey=ny)
  
    imx = ndimage.filters.convolve(im,gx)
    imy = ndimage.filters.convolve(im,gy)
    return imx, imy
    
def compute_harris_response(image):
    """ compute the Harris corner detector response function 
        for each pixel in the image"""
    kern_size = 3
    
    #derivatives
    imx,imy = gauss_derivatives(image, kern_size)
    
    #kernel for blurring
    gauss = gauss_kern(kern_size)

    #compute components of the structure tensor
    Wxx = ndimage.filters.convolve(imx*imx,gauss)
    Wxy = ndimage.filters.convolve(imx*imy,gauss)
    Wyy = ndimage.filters.convolve(imy*imy,gauss)

    #determinant and trace
    Wdet = Wxx*Wyy - Wxy**2
    Wtr = Wxx + Wyy
    
    
    return Wdet / Wtr
   
   
def get_harris_points(harrisim, min_distance=40, threshold=0.1):
    """ return corners from a Harris response image
        min_distance is the minimum nbr of pixels separating 
        corners and image boundary"""

    #find top corner candidates above a threshold
    corner_threshold = max(harrisim.ravel()) * threshold
    harrisim_t = (harrisim > corner_threshold) * 1

    #get coordinates of candidates
    candidates = array(harrisim_t.nonzero())
    
    coords = candidates.T
    
    #...and their values
    candidate_values = harrisim[coords[:,0],coords[:,1]]

    #sort candidates
    index = argsort(candidate_values)

    #store allowed point locations in array
    allowed_locations = zeros(harrisim.shape)
    allowed_locations[min_distance:-min_distance,min_distance:-min_distance] = 1

    # select the best points taking min_distance into account
    
    filtered_coords = []
    for i in index:
        if allowed_locations[coords[i][0],coords[i][1]] == 1:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i][0]-min_distance):(coords[i][0]+min_distance),(coords[i][1]-min_distance):(coords[i][1]+min_distance)] = 0

    return filtered_coords
    
def plot_harris_points(image, filtered_coords):
    """ plots corners found in image"""
    figure()
    gray()
    imshow(image)
    plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords],'*')
    axis('off')
    savefig("static_harris_file.png", transparent=True)  
    show()


def render_harris_points(image, filtered_coords):
    """This function renders points directly on an image with opencv"""
    pnts = [cv.cvPoint(int(i[1]),int(i[0])) for i in filtered_coords]
    for pnt in pnts:
        cv.cvCircle(image, pnt , 2, cv.CV_RGB(0,200,0),3 )

    
    
def static_test():
    """Takes a full colour numpy image"""
    from opencv import highgui
    image = highgui.cvLoadImage("/usr/share/doc/opencv-doc/examples/c/lena.jpg")
    
    
    result = adaptors.Ipl2NumPy(process_image(image))
    imshow(result)
   
    savefig("harris_scipy_static.png", transparent=True)
    show()


def process_image(image):
    """Carry out harris detection on a cvMat image with scipy"""
    np_image = adaptors.Ipl2NumPy(image)
    
    im = np_image.astype(uint8).mean(2)
    
    
    harrisim = compute_harris_response(im)                      # 150ms
    
    #filtered_coords = get_harris_points(harrisim, 6)            # 106ms 
    #render_harris_points(np_image, filtered_coords)             #   8ms
    #IPShellEmbed()()
    
    return filter_and_render_numpy(np_image,harrisim)
    #return np_image


def main():
   
    
    #static_test()

    title = "Harris Detector Output"
    VCP(process_image,title=title).main()
    

if __name__ == "__main__": 
    main()
