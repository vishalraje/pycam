# This is just a quickly hacked together script that pulls everything together.
# At the moment due to a buffer size problem in python (?) this only seems to work with ipython:
# ipython cross.py
# Brian Thorne 2009


import pygame
import pygame.camera
from pygame.locals import *
import numpy

import opencv
#from opencv import adaptors
import adaptors
from pygame import surfarray


from cvEyeTrack import Draw_Cross

print("Imported pygame, numpy, opencv and cvEyeTracking lib")
raw_input("Press Enter to capture an image (in pygame)")

pygame.init()
pygame.camera.init()
size = width,height = 640,480
display = pygame.display.set_mode(size,0)
camList = pygame.camera.list_cameras()                  # TODO: err if none found
camera = pygame.camera.Camera(camList[0],size,"RGB")
camera.start()
for i in range(100):
    if camera.query_image(): # ready to take an image?
        break
snapshot = camera.get_image()
camera.stop()


display.blit(snapshot,(0,0,))
pygame.display.flip()
pygame.display.flip()

print("Captured an image")
raw_input("Press Enter to convert into opencv format")

npy = surfarray.pixels3d(snapshot)
ipl = adaptors.NumPy2Ipl(npy)

print("Captured an image")
raw_input("Press Enter to pass to cvEyeTrack to add a cross")

green = opencv.CV_RGB(0,255,0)
Draw_Cross(ipl,200,200,50,100,green)

print("Added a cross")
raw_input("Press Enter to pass to back from opencv to pygame")

npy2 = adaptors.Ipl2NumPy(ipl)
npy2.transpose(1,0,2)

"""
In [2]: type(npy2)
Out[2]: <type 'numpy.ndarray'>

In [3]: npy2.shape
Out[3]: (640, 480, 3)
"""

snapshot2 = surfarray.make_surface(npy2)

print("Converted.")
raw_input("Press Enter to display the new image")

display.blit(snapshot2,(0,0))
pygame.display.flip()
pygame.display.flip()

raw_input("Press Enter to exit")

