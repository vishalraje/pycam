#!/usr/bin/python

## Living Pointillism - A world at motion is never clear
## by Nirav Patel <nrp@eclecti.cc>
##
## License - Do what you want, I'm dropping it into the public domain
##
## Requires pygame with camera module, from http://git.n0r.org/?p=pygame-nrp

import pygame, random
import pygame.camera
from pygame.locals import *

pygame.init()

class VideoCapturePlayer(object):
   size = ( 640, 480 )
   winsize = ( 700, 525 )
   def __init__(self, **argd):
       self.__dict__.update(**argd)
       super(VideoCapturePlayer, self).__init__(**argd)
       self.display = pygame.display.set_mode( self.winsize )
       pygame.display.set_caption("Living Pointillism")
       self.camera = pygame.camera.Camera("/dev/video0", self.size)
       self.camera.start()
       self.clock = pygame.time.Clock()
       self.maxpoint = int(self.winsize[0]/100)
       random.seed()
       self.snapshot = None
       self.frames = 0
      

   def get_and_flip(self):
       if self.snapshot:
           snapshot = self.camera.get_image(self.snapshot)
       else:
           self.snapshot = self.camera.get_image()
           snapshot = self.snapshot
       for z in range(max(20, int(self.frames*5))):
           x = random.random()
           y = random.random()
           rect = pygame.draw.circle(self.display, snapshot.get_at((int(x * self.size[0]),int(y * self.size[1]))), (int(x * self.winsize[0]),int(y * self.winsize[1])), random.randrange(2, self.maxpoint, 1), 0)
           pygame.display.update(rect)

   def main(self):
       going = True
       while going:
           events = pygame.event.get()
           for e in events:
               if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                   going = False

           self.get_and_flip()
           self.clock.tick()
           self.frames = self.clock.get_fps()
#           print self.frames

VideoCapturePlayer().main()
