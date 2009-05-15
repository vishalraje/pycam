import pygame
import pygame.camera
from pygame.locals import *
import numpy
pygame.init()
pygame.camera.init()
size = width,height = 640,480
display = pygame.display.set_mode(size,0)
camList = pygame.camera.list_cameras()                  # TODO: err if none found
camera = pygame.camera.Camera(camList[0],size,"RGB")
camera.start()
if camera.query_image(): # ready to take an image?
    snapshot = camera.get_image()
camera.stop()
display.blit(snapshot,(0,0,))
pygame.display.flip()
pygame.display.flip()
import opencv
from pygame import surfarray
npy = surfarray.pixels3d(snapshot)
ipl = opencv.adaptors.NumPy2Ipl(npy)
from cvEyeTrack import Draw_Cross
green = opencv.CV_RGB(0,255,0)
Draw_Cross(ipl,200,200,50,100,green)
npy2 = opencv.adaptors.Ipl2NumPy(ipl)
snapshot2 = surfarray.make_surface(npy2)
display.blit(snapshot2,(0,0))
pygame.display.flip()
pygame.display.flip()

