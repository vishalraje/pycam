#!/usr/bin/env python

"""
Load, Filter then Show an image with opencv in python
Brian Thorne 2009 <brian.thorne@hitlabnz.org>
"""

from VideoCapturePlayer import VideoCapturePlayer as VCP
from opencv import cv

def medianBlur(image, filterSize=43):
    """Blur an image with a particular strength filter.
    Note: Changes the original image, and returns the same pointer.
    
    
    >>> from median_opencv import medianBlur
    >>> from opencv import highgui
    >>> image_filename = "/usr/share/doc/opencv-doc/examples/c/lena.jpg"
    >>> i = highgui.cvLoadImage(image_filename)
    >>> blurred_image = medianBlur(i)
    >>> highgui.cvSaveImage("blurred_imag_python_opencv_median.jpg", blurred_image)
    1
    
    # Using pylab we can visually compare the pre and post filtered images:
    >>> from pylab import show, imread, imshow, figure, subplot, sum
    >>> i = imread("/usr/share/doc/opencv-doc/examples/c/lena.jpg")
    >>> b = imread("blurred_imag_python_opencv_median.jpg")
    >>> assert sum(i.flatten()) is not sum(b.flatten())
    >>> diff = b - i
    >>> assert sum(diff) > 0    # assert that the image changed
    >>> plot_ref = subplot(1,2,1)
    >>> plot_ref = imshow(b)
    >>> plot_ref = subplot(1,2,2)
    >>> plot_ref = imshow(i)
    >>> show() # show the images
    
    """
    cv.cvSmooth(image, image, cv.CV_MEDIAN, filterSize)
    return image

def testMedianBlur():
    """Test that the median blur function gives the exact same output
    in Python and in C++. Can run this test with:
    nosetests --with-doctest median_opencv.py -v
    
    Could potentially make another file for doing proper unit testing
    including building the cpp
    """
    from pylab import imread
    
    python_image = imread("blurred_imag_python_opencv_median.jpg")
    cpp_image = imread("blurred_imag_cpp_opencv_median.jpg")
    
    # For visual inspection:
    #from pylab import show, imshow, figure
    #imshow(python_image)
    #figure()
    #imshow(cpp_image)
    #show()
    
    return 0 == sum(python_image.flatten() - cpp_image.flatten())
    

if __name__ == "__main__":
    #testMedianBlur()
    title = "Median Filtered Output"
    VCP(medianBlur, title).main()
