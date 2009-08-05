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
       self.camera = X=pygame.camera.Camera("/dev/video0", self.size, "RGB")
       self.camera.start()
       self.clock = pygame.time.Clock()
       self.c = pygame.surface.Surface((640, 480), 0, 24)
       self.c.fill((0,0,0))
       self.c.set_colorkey((0,0,0))
       self.last = (0,0)
       self.snapshot = None
      

   def get_and_flip(self):
       if self.snapshot:
           snapshot = self.camera.get_image(self.snapshot)
       else:
           self.snapshot = self.camera.get_image()
           snapshot = self.snapshot
       
       a = pygame.surface.Surface((640, 480),0,24)
       b = pygame.surface.Surface((640, 480),0,24)
       pygame.camera.colorspace(snapshot, "HSV", b)
       b.fill((0,0,0),(0,470,640,480))
       pygame.transform.threshold(a, b, (75, 255, 155), (40, 100, 100), (255, 255, 255), True)
       a.unlock()   
       a.set_colorkey((255, 255, 255))
       mask = pygame.mask.from_surface(a)
       cc = mask.connected_component()
       cent = cc.centroid()
       a.unlock() 
       self.display.fill((0,0,0))
       self.display.blit(snapshot, (0,0))
       if self.last == (0,0):
           self.last = cent[0]
       pygame.draw.aaline(self.c, (0, 255, 0), self.last, cent[0])
       pygame.draw.circle(self.c, (0, 255, 0), cent[0], 2, 0)
       self.last = cent[0]
       self.display.blit(self.c, (0, 0))
       pygame.display.flip()

   def main(self):
       going = True
       self.get_and_flip()
       while going:
           events = pygame.event.get()
           for e in events:
               if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                   going = False

           self.get_and_flip()
           self.clock.tick(30)
#           print self.clock.get_fps()

VideoCapturePlayer().main()
