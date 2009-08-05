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
       self.overlay = pygame.Surface(self.size, 0, self.display)
       self.overlay.fill((0,0,0))
       self.overlay.set_colorkey((0,0,0))
       self.red = pygame.draw.rect(self.overlay, (255, 0, 0), (20,20,100,100), 2)
       self.green = pygame.draw.rect(self.overlay, (0, 255, 0), (270,20,100,100), 2)
       self.blue = pygame.draw.rect(self.overlay, (0, 0, 255), (520,20,100,100), 2)
       self.camera = X=pygame.camera.Camera("/dev/video0", self.size, "RGB")
       self.camera.start()
       self.clock = pygame.time.Clock()
       self.snapshot = None
       self.hsv = None
      

   def get_and_flip(self):
       if self.snapshot:
           snapshot = self.camera.get_image(self.snapshot)
       else:
           self.snapshot = self.camera.get_image()
           snapshot = self.snapshot
           self.hsv = pygame.Surface(self.size, 0, self.snapshot)
           
       pygame.camera.colorspace(snapshot, "HSV", self.hsv)
       red_color = pygame.transform.average_color(self.hsv,self.red)
       green_color = pygame.transform.average_color(self.hsv,self.green)
       blue_color = pygame.transform.average_color(self.hsv,self.blue)
       if red_color[0] < 50 and red_color[1] > 100:
           self.overlay.fill((255,0,0),self.red)
       if green_color[0] < 110 and green_color[0] > 80 and green_color[1] > 100:
           self.overlay.fill((0,255,0),self.green)
       if blue_color[0] < 170 and blue_color[0] > 130 and blue_color[1] > 100:
           self.overlay.fill((0,0,255),self.blue)
       print red_color , green_color , blue_color
       self.display.blit(self.snapshot, (0,0))
       self.display.blit(self.overlay, (0,0))
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
