# Some surface taking functions


from pycam import VideoCapturePlayer
from pygame import surfarray
import numpy
from scipy import signal


def outlineEdges(surface, laplacian_filter = numpy.array([[0,1,0],[1,-4,1],[0,1,0]])):
    gray_image = numpy.mean(surfarray.array3d(surface), 2)
    
    edges = signal.convolve2d(gray_image, laplacian_filter, mode="same")
    
    surf = surfarray.make_surface(edges)
    return surf
