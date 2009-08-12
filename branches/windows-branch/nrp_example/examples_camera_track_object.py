#!/usr/bin/python
import time
import pygame
import pygame.camera
from pygame.locals import *

pygame.init()

class VideoCapturePlayer(object):
   size = ( 640, 480 )
   def __init__(self, **argd):
       self.__dict__.update(**argd)
       super(VideoCapturePlayer, self).__init__(**argd)
       self.display = pygame.display.set_mode( self.size )
       self.camera = X=pygame.camera.Camera("/dev/video0", self.size, "HSV")
       self.camera.start()
       self.clock = pygame.time.Clock()
       self.snapshot = pygame.surface.Surface(self.size, 0, 24)
       self.overlay = pygame.surface.Surface(self.size, 0, 24)
       self.overlay.fill((0,0,0))
       self.overlay.set_colorkey((0,0,0))
       self.thresh = pygame.surface.Surface(self.size, 0, 24)
       self.thresh.set_colorkey((0,0,0))
       self.ccolor = None

      
   def calibrate(self):
       self.snapshot = self.camera.get_image(self.snapshot)
       self.display.blit(self.snapshot, (0,0))
       crect = pygame.draw.rect(self.display, (255,0,0), (300,220,40,40), 4)
       self.ccolor = pygame.transform.average_color(self.snapshot, crect)
       pygame.display.flip()

   def get_and_flip(self):
       self.snapshot = self.camera.get_image(self.snapshot)
       self.display.blit(self.snapshot, (0,0))
       pygame.transform.threshold(self.thresh, self.snapshot, self.ccolor, (20,25,25), (0,0,0), True)
       mask = pygame.mask.from_surface(self.thresh)
       cc = mask.connected_component()
       cent = cc.centroid()
       pos = cent[0]
       if cent[1] > 1000:
           cent = (0, 1000)
       pygame.draw.circle(self.overlay, (255,255,0), pos, cent[1]/100)
       self.display.blit(self.overlay, (0,0))
       pygame.display.flip()

   def main(self):
       going = True
       while going:
           events = pygame.event.get()
           for e in events:
               if e.type == KEYDOWN:
                   going = False
           self.calibrate()
       going = True
       while going:
           events = pygame.event.get()
           for e in events:
               if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                   going = False

           self.get_and_flip()
           self.clock.tick(30)
#           print self.clock.get_fps()

VideoCapturePlayer().main()
