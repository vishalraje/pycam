#!/usr/bin/python
from pycam import VideoCapturePlayer
from pycam import pygameFaceDetect
import pygame
from pygame.locals import *

def process(surf):
    faces = pygameFaceDetect.getFaces(surf)
    if faces:
        s = pygameFaceDetect.faceDetect.image_scale
        for face in faces:
            pointsInHat = [ (face.x*s, face.y*s),
                            (face.x*s + face.width*s, face.y*s),
                            (face.x*s + face.width*s/2, face.y*s - face.height*s/2 )   ]

            pygame.draw.polygon(surf, Color("black"), pointsInHat, 10)
            pygame.draw.polygon(surf, Color("red"), pointsInHat)
    return surf

if __name__ == "__main__":
    vcp = VideoCapturePlayer(processFunction=process)
    vcp.main()
    pygame.quit()
    
