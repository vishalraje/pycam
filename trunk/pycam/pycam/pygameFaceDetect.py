#!/usr/bin/python
"""
Uses pygame to take images from a live webcam, converts the numpy array to opencv format and uses 
the opencv library to detect faces, draws rectangles around each face with pygame, renders the finished image
with pygame.

"""

from pycam import VideoCapturePlayer
from pycam import ObjectDetector
import opencv

from pycam.conversionUtils import adaptors, surf2CV
import pygame
from pygame.locals import *
from pygame import surfarray
from IPython.Shell import IPShellEmbed

# While opencv has the image for detecting faces it can paint a rect 
# around the faces... Note pygame is still rendering the result
drawWithOpenCv = False

faceDetect = ObjectDetector('face')

def drawFacesOnSurface(surf, faces):
    """draw rectangles around detected cvObjects with pygame
    """
    s = faceDetect.image_scale
    for face in faces:
        r = pygame.Rect(face.x*s,face.y*s,face.width*s,face.height*s)
        pygame.draw.rect(surf,Color("green"),r,1)


def locateFacesProcess(surf):
    if drawWithOpenCv:
        img = surf2CV(surf)
        faceDetect.detect_and_draw(img)
        pygame.surfarray.blit_array(surf,cv2SurfArray(img))
    else:
        faces = getFaces(surf)
        if faces.total:
            # Break to shell when face is detected :-P
            #IPShellEmbed()()
            drawFacesOnSurface(surf,faces)
    return surf


def getFaces(surf):
    
    img = surf2CV(surf) #200ms!
    return faceDetect.detectObject(img)

def main():
    vcp = VideoCapturePlayer(processFunction=locateFacesProcess)
    vcp.main()
    pygame.quit()
    
if __name__ == "__main__":
    main()
    
