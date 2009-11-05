#!/usr/bin/python
"""
This example simply draws a red triangle above a detected face...
It requires OpenCV, Pygame and Pycam to be installed.

It could be improved with a kalman filter, opengl... you name it
"""
from __future__ import division
from pycam import VideoCapturePlayer
from pycam import pygameFaceDetect
import pygame
from pygame import gfxdraw, image, Rect, transform
from pygame.locals import *

try:
    hat = image.load('beanie.png')
except:
    pass

def drawAHat(surf, face):
    pointsInHat = [ (face.left, face.top),
                    (face.left + face.width, face.top),
                    (face.left + face.width/2, face.top - face.height/2 )]
    gfxdraw.filled_polygon(surf, pointsInHat, Color("red"))
    gfxdraw.aapolygon(surf, pointsInHat, Color("black"))

def overlayAHat(surf, face):
    # Draw an image of a hat on top of the face.
    width_factor, height_factor = 5/5, 3/5
    scaled_hat = transform.scale(hat, (int(width_factor*face.width), int(height_factor*face.height)))
    hat_x = int(face.left + (face.width/2) - width_factor*face.width/2)    
    hat_y = int(face.top - height_factor*face.height/2)
    surf.blit(scaled_hat, (hat_x, hat_y))
    
def drawHatOnFaces(surf):
    faces = pygameFaceDetect.getFaces(surf)
    if faces:
        s = pygameFaceDetect.faceDetect.image_scale
        for face in faces:
            bounding_rect = Rect(face.x*s, face.y*s, face.width*s, face.height*s)
            #pygame.draw.rect(surf, Color("blue"), bounding_rect, 2)
            try:
                overlayAHat(surf, bounding_rect)
            except NameError:
                drawAHat(surf, bounding_rect)

    return surf

if __name__ == "__main__":
    VideoCapturePlayer(processFunction=drawHatOnFaces).main()
    
    
