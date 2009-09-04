import numpy as np
from scipy import signal

from opencv import adaptors

def opencvFilt2sigma(size):
    """OpenCV defaults to making sigma up with this formula.
    Learning OpenCV: computer vision with the OpenCV library
    By Gary Bradski, Adrian Kaehler pg 112"""
    return (( size*0.5 ) - 1)*0.30 + 0.80

class scipyFromOpenCV(object):
    """This decorator can be used to wrap a function that takes 
    and returns a numpy array into one that takes and retuns an
    opencv CvMat.
    """
    def __init__(self, f):
        self.f = f    

    def __call__(self, image):
        # Convert CvMat to ndarray
        np_image = adaptors.Ipl2NumPy(image)
        
        # Call the original function
        np_image_filtered = self.f(np_image)
        
        # Convert back to CvMat
        return adaptors.NumPy2Ipl(np_image_filtered)


def convert_to_8bit_3chan(image):    
    result = cv.cvCreateMat(image.rows, image.cols, cv.CV_8UC3)
    cv.cvConvertScale(image, result)
    return result


def convert_to_grey(image):
    result = cv.cvCreateMat(image.rows, image.cols, cv.CV_8UC1)
    cv.cvCvtColor(image,result,cv.CV_BGR2GRAY)  # convert to gray scale
    return result


###########################
# This is very slow.
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

@scipyFromOpenCV
def slowGaussianBlur(matrix):
    """Manual gaussian blur - Very very very slow!"""
    filterSize = 43
    filt = gauss_kern(filterSize)

    r = signal.convolve(matrix[:,:,0],filt,'same')
    g = signal.convolve(matrix[:,:,1],filt,'same')
    b = signal.convolve(matrix[:,:,2],filt,'same')
    
    result = array([r,b,g]).astype(uint8).transpose((1,2,0))
   
    return result
#########################




