#!/usr/bin/env python
"""
Show an image and filter with scipy in python
Brian Thorne - July 09
Compile/Run with: python blur_scipy.py
"""

from __future__ import division
import numpy as np
from numpy import array, uint8
from scipy import signal, ndimage
from VideoCapturePlayer import VideoCapturePlayer as VCP
from misc import scipyFromOpenCV, opencvFilt2sigma


@scipyFromOpenCV
def gaussianBlur(np_image):
    """Blur an image with scipy"""
    sigma = opencvFilt2sigma(43.0)
    
    result = ndimage.filters.gaussian_filter(np_image, 
                            sigma=(sigma, sigma, 0),
                            order=0,
                            mode='reflect'
                            )
    return result

@scipyFromOpenCV
def gaussianBlur3Way(np_image, sigma=opencvFilt2sigma(43.0)):
    """Blur an image with scipy using 3 seperate gaussian filters
    This is equivalent to the above function"""
    
    r = ndimage.filters.gaussian_filter(np_image[:,:,0], sigma=(sigma, sigma))
    g = ndimage.filters.gaussian_filter(np_image[:,:,1], sigma=(sigma, sigma))
    b = ndimage.filters.gaussian_filter(np_image[:,:,2], sigma=(sigma, sigma))

    return array([r,g,b]).transpose((1,2,0))


#############
# From the scipy mailing list

from numpy import array, zeros, ones, flipud, fliplr
from scipy.signal import lfilter
from math import sqrt

def __gausscoeff(s):

   # Young, I.T. and van Vliet, L.J. (1995). Recursive implementation
   # of the Gaussian filter, Signal Processing, 44: 139-151.

   if s < .5: raise ValueError, \
       'Sigma for Gaussian filter must be >0.5 samples'
   q = 0.98711*s - 0.96330 if s > 0.5 else 3.97156 \
       - 4.14554*sqrt(1.0 - 0.26891*s)
   b = zeros(4)
   b[0] = 1.5785 + 2.44413*q + 1.4281*q**2 + 0.422205*q**3
   b[1] = 2.44413*q + 2.85619*q**2 + 1.26661*q**3
   b[2] = -(1.4281*q**2 + 1.26661*q**3)
   b[3] = 0.422205*q**3
   B = 1.0 - ((b[1] + b[2] + b[3])/b[0])

   # convert to a format compatible with lfilter's
   # difference equation

   B = array([B])
   A = ones(4)
   A[1:] = -b[1:]/b[0]
   return B,A

def gaussian1D(signal, sigma, padding=0):
   n = signal.shape[0]
   tmp = zeros(n + padding)
   if tmp.shape[0] < 4: raise ValueError, \
       'Signal and padding too short'
   tmp[:n] = signal
   B,A = __gausscoeff(sigma)
   tmp = lfilter(B, A, tmp)
   tmp = tmp[::-1]
   tmp = lfilter(B, A, tmp)
   tmp = tmp[::-1]
   return tmp[:n]

def gaussian2D(image, sigma, padding=0):
   n,m = image.shape[0],image.shape[1]
   tmp = zeros((n + padding, m + padding))
   if tmp.shape[0] < 4 or tmp.shape[1] < 4: raise ValueError, \
       'Image and padding too small'
   B,A = __gausscoeff(sigma)
   tmp[:n,:m] = image
   tmp = lfilter(B, A, tmp, axis=0)
   tmp = flipud(tmp)
   tmp = lfilter(B, A, tmp, axis=0)
   tmp = flipud(tmp)
   tmp = lfilter(B, A, tmp, axis=1)
   tmp = fliplr(tmp)
   tmp = lfilter(B, A, tmp, axis=1)
   tmp = fliplr(tmp)
   return tmp[:n,:m]
   
@scipyFromOpenCV
def mlGaussianBlur(image):   
    return gaussian2D(image[:,:,1], 0.6)
########



def testGaussianBlur():
    """Test that the guassian blur function gives the exact same output
    in Python and in C++ with OpenCV and with SciPy. Can run this test with:
    nosetests --with-doctest blur_scipy.py -v
    """
    from pylab import imread
    from opencv import highgui
    import blur_opencv
    
    # Using Lena image create tests image.
    image_filename = "/usr/share/doc/opencv-doc/examples/c/lena.jpg"
    i = highgui.cvLoadImage(image_filename)
    
    # Carry out the bluring
    py_scipy = gaussianBlur3Way(i)
    py_scipy2 = gaussianBlur(i)
    py_opencv = blur_opencv.gaussianBlur(i)
    
    # Save the outputs as jpg files
    highgui.cvSaveImage("blurred_imag_python_scipy_gaussian.jpg", py_scipy)
    highgui.cvSaveImage("blurred_imag_python_scipy2_gaussian.jpg", py_scipy2)
    highgui.cvSaveImage("blurred_imag_python_opencv_gaussian.jpg", py_opencv)
    
    # Load in the image data with scipy
    python_opencv_image = imread("blurred_imag_python_opencv_gaussian.jpg")
    python_scipy_image = imread("blurred_imag_python_scipy_gaussian.jpg")
    python_scipy2_image = imread("blurred_imag_python_scipy2_gaussian.jpg")
    
    diff = python_opencv_image - python_scipy_image
    diff2 = python_opencv_image - python_scipy2_image
    diff3 = python_scipy_image - python_scipy2_image
    
    # For visual inspection:
    
    from pylab import show, imshow, figure, subplot, title
    """
    figure()
    subplot(1,3,1); title("The OpenCV Output (Py and C++)")
    imshow(python_opencv_image)
    subplot(1,3,2); title("3 way ndimage filter")
    imshow(python_scipy_image)
    subplot(1,3,3); title("SciPy: ndimage.filters.gaussian_filter")
    imshow(python_scipy2_image)
    figure()
    subplot(1,3,1)
    imshow(diff)
    subplot(1,3,2)
    imshow(diff2)
    subplot(1,3,3)
    imshow(diff3)
    """
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    
    
    plt.figure()
    plt.title("Pixel by pixel difference of one row from image in Scipy and OpenCV Gaussian Filter")
    plt.plot(diff[:,50,1])
    
    plt.figure()
    plt.subplot(1,3,1)
    plt.title("R")
    im1 = plt.imshow(diff[:,:,0])
    CB1 = plt.colorbar(im1, orientation='horizontal')
    plt.subplot(1,3,2)
    plt.title("G")
    im2 = plt.imshow(diff[:,:,1], cmap=cm.gray)
    CB2 = plt.colorbar(im2, orientation='horizontal')
    plt.subplot(1,3,3)
    plt.title("B")
    im3 = plt.imshow(diff[:,:,2], cmap=cm.gray)
    CB3 = plt.colorbar(im3, orientation='horizontal')
    
    #plt.figure()
    #im = plt.imshow(python_opencv_image[:,:,2], cmap=cm.gray)
    
    show()
    
    # Check that the sum of all differences at each point is 0
    print sum(python_opencv_image.flatten() - python_scipy_image.flatten())

def main():
    title = "SciPy Guassian Filtered Output"
    #VCP(mlGaussianBlur,title=title).main()
    VCP(gaussianBlur,title=title).main()
    #VCP(slowGaussianBlur,title=title).main()

if __name__ == "__main__": 
    #testGaussianBlur()
    main()
    #import cProfile
    #cProfile.run("main()",'python_profile_data')

