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
    
    figure()
    title("Pixel by pixel difference in Scipy and OpenCV Gaussian Filter")
    imshow(diff)
    show()
    
    # Check that the sum of all differences at each point is 0
    print sum(python_opencv_image.flatten() - python_scipy_image.flatten())

def main():
    title = "SciPy Guassian Filtered Output"
    VCP(gaussianBlur,title=title).main()
    #VCP(slowGaussianBlur,title=title).main()

if __name__ == "__main__": 
    testGaussianBlur()
    main()
    #import cProfile
    #cProfile.run("main()",'python_profile_data')

