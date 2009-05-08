#!/usr/bin/python

import opencv
import pygame
from VideoCapturePlayer import *
from conversionUtils import *

from objectDetect import ObjectDetector

def locatePeopleProcess(surf):
    person = False
    for detector in detectors:
        # Try detect anything at all!
        cvMat = surf2CV(surf)
        objects = detector.detectObject(cvMat)
        if objects:
            person = True
            break
    if person:
        
        print "There is a person in front of this computer"
    else:
        print "There is noone at this computer"

if __name__ == "__main__":
#    eyeDetector = ObjectDetector("eye")
    detectors = [ 
               #  ObjectDetector("head"),
              #   ObjectDetector("face"),
                 ObjectDetector("upperbody"),
                 ]
    
    vcp = VideoCapturePlayer(processFunction=locatePeopleProcess,show=False)
    vcp.main()
    pygame.quit()