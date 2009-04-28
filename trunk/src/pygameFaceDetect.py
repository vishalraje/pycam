#!/usr/bin/python
from VideoCapturePlayer import *
import faceDetect
import opencv
#from opencv 
import adaptors
import pygame
from pygame.locals import *
from pygame import surfarray

# While opencv has the image for detecting faces it can paint a rect 
# around the faces...
drawWithOpenCv = True

def drawFacesOnSurface(surf,faces):
    """draw rectangles around detected cvObjects with pygame
    """
    s = faceDetect.image_scale
    for face in faces:
        r = pygame.Rect(face.x*s,face.y*s,face.width*s,face.height*s)
        pygame.draw.rect(surf,Color("green"),r,1)
    
def locateFacesProcess(surf):
    if drawWithOpenCv:
        numpyImage = surfarray.pixels3d(surf)
        cvImage = adaptors.NumPy2Ipl(numpyImage.transpose(1,0,2))
        faceDetect.detect_and_draw(cvImage)
        numpyImage = adaptors.Ipl2NumPy(cvImage)
        surfarray.blit_array(surf,numpyImage.transpose(1,0,2))
    else:
        faces = getFaces(surf)
        if faces:
            drawFacesOnSurface(surf,faces)
    
    return surf

def getFaces(surf):
    return faceDetect.detectObject(adaptors.NumPy2Ipl(surfarray.pixels3d(surf).transpose(1,0,2)))

if __name__ == "__main__":
    vcp = VideoCapturePlayer(processFunction=locateFacesProcess)
    vcp.main()
    pygame.quit()
    