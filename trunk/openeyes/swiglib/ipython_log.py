#log# Automatic Logger file. *** THIS MUST BE THE FIRST LINE ***
#log# DO NOT CHANGE THIS LINE OR THE TWO BELOW
#log# opts = Struct({'__allownew': True, 'log': 1, 'logfile': 'ipython_log.py'})
#log# args = ['drawCross.py']
#log# It is safe to make manual edits below here.
#log#-----------------------------------------------------------------------
_ip.magic("logstart ")
import pygame
import pygame.camera
from pygame.locals import *
import numpy
pygame.init()
pygame.camera.init()
size = width,height = 640,480
display = pygame.display.set_mode(size,0)
camList = pygame.camera.list_cameras()                  # TODO: err if none found
camera = pygame.camera.Camera(camList[0],size,"RGB")    # starting in RGB mode - this means frame comes in size (640,480,3) (1MB each?)
camera.start()
camera.query_image() # ready to take an image?
snapshot = camera.get_image()
camera.stop()
display.blit(snapshot,(0,0,))
pygame.display.flip()
pygame.display.flip()
import opencv
from pygame import surfarray
npy = surfarray.pixels3d(snapshot)
ipl = opencv.adaptors.NumPy2Ipl(npy)
import CvEyeTrack
import vEyeTrack
import cvEyeTrack
from cvEyeTrack import Draw_Cross
#?Draw_Cross
green = opencv.CV_RGB(0,255,0)
green
Draw_Cross(ipl,200,200,50,100,green)
npy2 = opencv.adaptors.Ipl2NumPy(ipl)
snapshot2 = surfarray.make_surface(npy2)
display.blit(snapshot2,(0,0))
pygame.display.flip()
pygame.display.flip()
_ip.magic("logoff ")
