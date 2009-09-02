import numpy as np
from scipy import signal
from opencv import adaptors

def gauss_kern(size, sizey=None):
    """ Returns a normalized 2D gauss kernel array for convolutions."""
    size = int(size)
    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)
    x, y = np.mgrid[-size:size+1, -sizey:sizey+1]
    g = np.exp(-(x**2/float(size) + y**2/float(sizey)))
    return g / g.sum()

def convert_to_8bit_3chan(image):    
    result = cv.cvCreateMat(image.rows, image.cols, cv.CV_8UC3)
    cv.cvConvertScale(image, result)
    return result


def convert_to_grey(image):
    result = cv.cvCreateMat(image.rows, image.cols, cv.CV_8UC1)
    cv.cvCvtColor(image,result,cv.CV_BGR2GRAY)  # convert to gray scale
    return result


class scipyFromOpenCV(object):

    def __init__(self, f):
        self.f = f
        

    def __call__(self, image):
        # Convert CvMat to ndarray
        np_image = adaptors.Ipl2NumPy(image)
        
        # Call the original function
        np_image_filtered = self.f(np_image)
        
        # Convert back to CvMat
        return adaptors.NumPy2Ipl(np_image_filtered)
        
