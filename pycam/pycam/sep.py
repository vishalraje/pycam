from VideoCapturePlayer import VideoCapturePlayer as VCP
from pygame import surfarray
import numpy
from scipy import ndimage
from pylab import *

import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.figure()
show()

def plot_seperate_rgb(diff):
    plt.subplot(1,3,1)
    plt.title("R")
    im1 = plt.imshow(diff[:,:,0], cmap=cm.Reds)
    CB1 = plt.colorbar(im1, orientation='horizontal')
    plt.subplot(1,3,2)
    plt.title("G")
    im2 = plt.imshow(diff[:,:,1], cmap=cm.Greens)
    CB2 = plt.colorbar(im2, orientation='horizontal')
    plt.subplot(1,3,3)
    plt.title("B")
    im3 = plt.imshow(diff[:,:,2], cmap=cm.Blues)
    CB3 = plt.colorbar(im3, orientation='horizontal')
    
def someProcess(imageSurface):
    np_array = surfarray.array3d(imageSurface)
    
    plot_seperate_rgb(np_array.transpose((1,0,2)))
    
    surf = imageSurface #surfarray.make_surface(result)
    
    return surf
    
vcp = VCP(processFunction=someProcess)
vcp.main()
