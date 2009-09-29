#!/usr/bin/python
"""This example doesn't actually display anything - but it prints out
if it finds a face at the computer or not."""
import opencv
import pygame
from pycam import VideoCapturePlayer
from pycam.conversionUtils import *

from pycam.objectDetect import ObjectDetector

def locatePeopleProcess(surf, lastState=[]):
    person = False
    for detector in detectors:
        # Try detect anything at all!
        cvMat = surf2CV(surf)
        objects = detector.detectObject(cvMat)
        for o in objects:
            if o:
                person = True
                break
    lastState.append(person)
    if len(lastState)> 3 and lastState[-1] is not lastState[-2]:
        if person:
            print "There is a person in front of this computer"
        else:
            print "There is no one at this computer"

if __name__ == "__main__":
#    eyeDetector = ObjectDetector("eye")
    detectors = [ 
                 ObjectDetector("head"),
                 ObjectDetector("face"),
                 ObjectDetector("upperbody"),
                 ]
    
    vcp = VideoCapturePlayer(processFunction=locatePeopleProcess,show=False)
    vcp.main()
    pygame.quit()
