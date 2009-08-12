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

       self.snapshot = None
      

   def get_and_flip(self):
       if self.snapshot:
           snapshot = self.camera.get_image(self.snapshot)
       else:
           self.snapshot = self.camera.get_image()
           snapshot = self.snapshot

       color = pygame.transform.average_color(snapshot)
       self.display.fill(color)
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
