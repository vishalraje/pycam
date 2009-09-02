# Show an image and filter with scipy in python
# Brian Thorne - July 09
# Compile/Run with: python medianFilterScipy.py

from scipy import signal, random, misc
from matplotlib import pylab    # Just for something differant - will display output with matplotlib

image = pylab.imread('image.png')    # need a png unless we have PIL installed

image_noisy = image + random.normal(size=image.shape )    # Add some noise

imageFiltered = signal.medfilt2d(image_noisy, 9)

pylab.imshow(imageFiltered)    # Note now showing the image in matplotlib
pylab.show()
