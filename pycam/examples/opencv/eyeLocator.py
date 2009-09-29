#!/usr/bin/python

import opencv
import pygame
from pycam import VideoCapturePlayer
from pycam.conversionUtils import *
from pycam.pygameFaceDetect import getFaces
from pycam.objectDetect import ObjectDetector
from pygame.locals import *

eyeDetector = ObjectDetector("eye")

def locateFaceAndEyeProcess(surf):
    faces = getFaces(surf)
    
    s = eyeDetector.image_scale 
    
    if faces:
        for face in faces:
            r = pygame.Rect(face.x*s,face.y*s,face.width*s,face.height*s)
            pygame.draw.rect(surf,Color("green"),r,1)
            facialSurf = surf.subsurface(r)
            facialCvMat = surf2CV(facialSurf)
            eyeDetector.detect_and_draw(facialCvMat)
            pygame.surfarray.blit_array(facialSurf,cv2SurfArray(facialCvMat))
    return surf

if __name__ == "__main__":
    vcp = VideoCapturePlayer(processFunction=locateFaceAndEyeProcess,forceOpenCv=True)
    vcp.main()
    pygame.quit()
